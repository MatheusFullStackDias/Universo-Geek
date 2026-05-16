from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from universogeek.models import Usuario


class FormsLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Passoword", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("E-mail inexistente, crie uma conta.")


class FormsCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    senha_validacao = PasswordField("Password confirmation ", validators=[DataRequired(), EqualTo("senha")])
    username = StringField("username", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já casdratado, faça login para continuar.")

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("esse Username já existe, crie outro.")


class FormsFotos(FlaskForm):
    foto = FileField("Fotos", validators=[DataRequired()])
    botao_enviar = SubmitField("Enviar")

