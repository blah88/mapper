from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

bcrypt = Bcrypt()
db = SQLAlchemy()

DB_NAME = "mapper"

def create_app():

    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False
    app.config['SECRET_KEY'] = 'duck'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:Trello1?@mapper.c9nhahuxgile.ap-southeast-2.rds.amazonaws.com:5432/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    from commands import db_commands
    app.register_blueprint(db_commands)
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'duck'

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.environ.get("DB_URI")

        if not value:
            raise ValueError("DB_URI is not set")

        return value

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        value = os.environ.get("SECRET_KEY")

        if not value:
            raise ValueError("Secret Key is not set")
        
        return value


class TestingConfig(Config):
    TESTING = True

environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
