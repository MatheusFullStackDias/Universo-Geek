from universogeek import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))



class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True )
    username = database.Column(database.String(30), nullable=False, unique=True)
    email = database.Column(database.String(120), nullable=False, unique=True)
    senha = database.Column(database.String(60), nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)
    image_file = database.Column(database.String(500), nullable=False, default='default.jpg')


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagen = database.Column(database.String, default='defaut.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)

