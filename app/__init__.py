from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .config import config_by_name

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def creat_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app
