from flask import render_template,url_for, redirect, request, current_app, flash, abort
from universogeek import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from universogeek.forms import FormsLogin, FormsCriarConta, FormsFotos
from universogeek.models import Usuario, Foto
import os
from secrets import token_hex
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormsLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarConta():
    formCriarConta = FormsCriarConta()
    if formCriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data)
        usuario = Usuario(username=formCriarConta.username.data,
                          senha=senha,
                          email=formCriarConta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarConta.html", form=formCriarConta)

@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        #O USUARIO ESTA VENDO O PERFIL DELE
        formsfotos = FormsFotos()
        if formsfotos.validate_on_submit():
            arquivo = formsfotos.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # Salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"],
                                   nome_seguro)
            arquivo.save(caminho)
            # Registrar o arquivo no banco de dados
            foto = Foto(imagen=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for('perfil', id_usuario=current_user.id))
        return render_template("perfil.html", usuario=current_user, form=formsfotos)
    else:
        usuario = Usuario.query.get(int(id_usuario))
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

            # 2. Gerar um nome aleatório para evitar nomes duplicados
            random_hex = token_hex(8)
            _, f_ext = os.path.splitext(arquivo.filename)
            nome_final = random_hex + f_ext

            # 3. Caminho onde a foto será salva
            caminho_completo = os.path.join(current_app.root_path, 'static/foto_perfil', nome_final)

            # 4. Salvar o arquivo no disco
            arquivo.save(caminho_completo)

            # 5. Atualizar o banco de dados do usuário logado
            current_user.image_file = nome_final
            database.session.commit()

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
