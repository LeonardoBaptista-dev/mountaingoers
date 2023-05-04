from mountaingoers import database, app
from mountaingoers.models import Usuario, Foto

with app.app_context():
    database.create_all()
