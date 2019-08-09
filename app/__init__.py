from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

from .admin import _Admin
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()
toolbar = DebugToolbarExtension()


def create_app(config_name):
    app = Flask(__name__)

    admin = _Admin()
    app.config.from_object(config.get(config_name)) or config['default']

    bootstrap.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Flask and Flask-SQLAlchemy initialization here

    from .models import User, Role
    admin.add_model_views([
        User, Role
    ], db)

    return app
