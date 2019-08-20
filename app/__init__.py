from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager


from config import config
from .admin import Admin, SecuredHomeView

bootstrap = Bootstrap()
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
admin = Admin(template_mode='bootstrap4', base_template='/admin/new_master.html')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config.get(config_name)) or config['default']

    bootstrap.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app, index_view=SecuredHomeView())

    from app import blueprints
    blueprints.init_app(app)

    return app
