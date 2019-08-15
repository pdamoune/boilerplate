from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors  # nopep8
from ..models import Permission  # nopep8


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
