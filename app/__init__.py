from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager


from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()
toolbar = DebugToolbarExtension()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config.get(config_name)) or config['default']

    bootstrap.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from app import blueprints
    blueprints.init_app(app)

    return app
