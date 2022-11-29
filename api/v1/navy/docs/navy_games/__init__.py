from flask import Blueprint

navy_game_sw = Blueprint("navy_game_sw", __name__)


from . import views
