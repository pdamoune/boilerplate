from .models import User, Role
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .admin import _Admin
from app import db


def init_app(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    admin = _Admin()
    admin.init_app(app)
    admin.add_model_views([
        User, Role
    ], db)
