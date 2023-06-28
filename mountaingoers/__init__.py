from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.sqlite"
app.config["SECRET_KEY"] = "34ed0d7581bb07244c7b478490d92eb8"
app.config["UPLOAD_FOLDER"] = "static/img/posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"


from mountaingoers import routes
