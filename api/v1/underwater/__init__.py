from flask import Blueprint

underwater = Blueprint("underwater", __name__)

from . import views
