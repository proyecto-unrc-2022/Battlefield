from flask import jsonify, request

from app import db
from app.daos.navy.game_dao import add_game
from app.models.navy.dynamic_navy_models import Game
from app.navy.navy_constants import PATH_TO_START
from app.navy.navy_game_control import NavyGameControl

from . import navy


@navy.post("/create")
def create_game():
    id_game = add_game(request.json["id_user_1"])
    json_resp = NavyGameControl.read_data(PATH_TO_START)
    json_resp["game_id"] = id_game
    return jsonify(json_resp)


@navy.post("/start")
def start_game():
    pass
