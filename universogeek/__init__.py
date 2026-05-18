from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://banco_geek_user:H74VjtahUxwdyF7UB9tKoFx693F1Njmo@dpg-d84adcbrjlhs73d3cidg-a.oregon-postgres.render.com/banco_geek"
app.config["SECRET_KEY"] = "b61a43b56f5898ecf8855b186fc2fa2c"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

from universogeek import routes