from flask import Blueprint

navy_game_action_sw = Blueprint("navy_game_action_sw", __name__)

from . import views
