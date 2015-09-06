from flask import Blueprint

magazines = Blueprint('magazines', __name__)

from . import views, errors
