from flask import Blueprint

navy = Blueprint("navy", __name__)

from . import views
