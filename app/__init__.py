from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
# cli.CustomCli.init_app(app)
from config import config
from .admin import _Admin


bootstrap = Bootstrap()
toolbar = DebugToolbarExtension()
db = SQLAlchemy()
admin = _Admin()


def create_app(config_name):
    app = Flask(__name__)

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
