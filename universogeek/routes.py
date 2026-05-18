from flask import render_template,url_for, redirect, request, current_app, flash, abort
from universogeek import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from universogeek.forms import FormsLogin, FormsCriarConta, FormsFotos
from universogeek.models import Usuario, Foto
import os
from secrets import token_hex
from werkzeug.utils import secure_filename
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://muklibpouqlxhlkcngob.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_GcG5B0U-24yoUu3lBrU29w_ZlOU8Pic")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormsLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarConta():
    formCriarConta = FormsCriarConta()
    if formCriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data).decode("utf-8")
        usuario = Usuario(username=formCriarConta.username.data,
                          senha=senha,
                          email=formCriarConta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarConta.html", form=formCriarConta)

@app.route("/perfil/<int:id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    # Mudança preventiva: usando int direto no parâmetro da rota (<int:id_usuario>)
    # evita erros caso o navegador envie textos acidentalmente para cá.
    if id_usuario == current_user.id:
        # O USUARIO ESTA VENDO O PERFIL DELE
        formsfotos = FormsFotos()

        if formsfotos.validate_on_submit():
            arquivo = formsfotos.foto.data
            nome_seguro = secure_filename(arquivo.filename)

            # --- MUDANÇA PARA O SUPABASE ---
            # 1. Ler os dados binários do arquivo para enviar para a nuvem
            dados_arquivo = arquivo.read()

            # 2. Enviar o arquivo para a raiz do seu bucket 'fotos_posts'
            supabase.storage.from_("fotos_posts").upload(
                path=nome_seguro,
                file=dados_arquivo,
                file_options={"content-type": arquivo.content_type}
            )

            # 3. Buscar a URL pública completa do arquivo que acabou de subir
            url_publica = supabase.storage.from_("fotos_posts").get_public_url(nome_seguro)

            # 4. Registrar a URL COMPLETA no banco de dados
            foto = Foto(imagen=url_publica, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            # ---------------------------------

            return redirect(url_for('perfil', id_usuario=current_user.id))

        return render_template("perfil.html", usuario=current_user, form=formsfotos)
    else:
        usuario = Usuario.query.get_or_404(id_usuario)
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/avatar", methods=["GET", "POST"])
@login_required
def avatar():
    if request.method == 'POST':
        if request.files.get('foto_perfil'):
            # 1. Pegar o arquivo enviado
            arquivo = request.files['foto_perfil']

            # 2. Gerar um nome seguro e aleatório para a foto
            random_hex = token_hex(8)
            _, f_ext = os.path.splitext(arquivo.filename)
            nome_final = f"{random_hex}{f_ext}"

            # 3. Ler os dados binários do arquivo (diretamente da memória, sem salvar no disco)
            dados_arquivo = arquivo.read()
            caminho_no_bucket = f"{nome_final}"

            # 4. Fazer o upload para o bucket do Supabase
            supabase.storage.from_("fotos_posts").upload(
                path=caminho_no_bucket,
                file=dados_arquivo,
                file_options={"content-type": arquivo.content_type}
            )

            # 5. Buscar a URL pública gerada pelo Supabase
            url_publica = supabase.storage.from_("fotos_posts").get_public_url(caminho_no_bucket)

            # 6. Atualizar a coluna do usuário com a URL completa e salvar no banco de dados
            current_user.image_file = url_publica
            database.session.commit()

            # Aplicando o padrão PRG para evitar duplicação ao atualizar a página (F5)
            return redirect(url_for('perfil', id_usuario=current_user.id))

    return render_template("fotoPerfil.html", usuario=current_user)

@app.route("/feed")
@login_required
def feed():
    fotos =  Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)


@app.route("/foto/excluir/<int:id_foto>", methods=["POST"])
@login_required
def excluir_foto(id_foto):
    # 1. Buscar a foto no banco de dados pelo ID
    foto = Foto.query.get_or_404(id_foto)

    # 2. SEGURANÇA: Verificar se o usuário logado realmente é o dono da foto
    if foto.id_usuario != current_user.id:
        abort(403)  # Bloqueia o acesso se não for o dono (Erro de Proibido)

    try:
        # 3. Encontrar o caminho do arquivo físico no servidor e deletá-lo
        caminho_foto = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    app.config["UPLOAD_FOLDER"],
                                    foto.imagen)

        # Verifica se o arquivo realmente existe na pasta antes de tentar deletar
        if os.path.exists(caminho_foto):
            os.remove(caminho_foto)

        # 4. Deletar o registro da foto no banco de dados
        database.session.delete(foto)
        database.session.commit()

        flash("Foto excluída com sucesso!", "sucesso")
    except Exception as e:
        database.session.rollback()
        flash("Erro ao tentar excluir a foto.", "erro")

    # 5. Redireciona o usuário de volta para o perfil dele
    return redirect(url_for('perfil', id_usuario=current_user.id))
