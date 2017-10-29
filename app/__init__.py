from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os

db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.signing'
login_manager.login_message = 'Please, log in to access this page.'


def create_app(config_name):

    """Initialize of application"""

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.reflect(engine)
    db.init_app(app)

    mail.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
