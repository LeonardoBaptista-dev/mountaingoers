from datetime import datetime
from mountaingoers import database
from flask_login import UserMixin # Determina qual é class que vai gerenciar a estrutura de login
from mountaingoers import app
from mountaingoers import app, login_manager
from . import database





#função obrigatória que recebe o id de um usuario, e precisa retornar quem é esse usuario procurando no database

@login_manager.user_loader
def Load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))
    


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.String, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
