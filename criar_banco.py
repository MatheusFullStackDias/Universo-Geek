from universogeek import database, app
from universogeek.models import Usuario, Foto

with app.app_context():
    database.create_all()