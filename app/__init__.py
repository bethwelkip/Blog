from config import config_options
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
import sys


mail = Mail()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    return app

