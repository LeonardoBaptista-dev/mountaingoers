#Criando as rotas e funções do projeto

from flask import Flask, render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from mountaingoers import app, database, bcrypt
from mountaingoers.forms import FormCadastro, FormLogin, FormFoto
from mountaingoers.models import Usuario,Foto
from werkzeug.utils import secure_filename
import os


@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario,remember=True)   
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)

@app.route("/perfil/<id_usuario>", methods=["GET","POST"])
@login_required
def perfil(id_usuario):
    #o usuario está vendo seu próprio perfil
    if int(id_usuario) == int(current_user.id):
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            #salva o arquivo na pasta posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                   app.config["UPLOAD_FOLDER"],nome_seguro)
            arquivo.save(caminho)
            #registrar esse arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form=formfoto)
    else:

        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    formcadastro = FormCadastro()    
    if formcadastro.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcadastro.senha.data) 
        usuario = Usuario(username=formcadastro.username.data, 
                          senha=senha, 
                          email=formcadastro.email.data)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario,remember=True)   
        return redirect(url_for("perfil", id_usuario=usuario.id))
        
    return render_template("cadastro.html", form=formcadastro)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
    

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)

