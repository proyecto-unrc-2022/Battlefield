from flask import Blueprint

missile_sw = Blueprint("missile_sw", __name__)

from . import views
