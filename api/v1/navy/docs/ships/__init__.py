from flask import Blueprint

ship_sw = Blueprint("ship_sw", __name__)

from . import views
