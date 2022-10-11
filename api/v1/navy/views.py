from flask import jsonify, request
from app.navy.utils.navy_response import NavyResponse
from marshmallow import ValidationError

from api import token_auth
from app import db
from app.daos.navy.dynamic_ship_dao import add_ship
from app.daos.navy.game_dao import add_game, get_game, read_data
from app.models.navy.dynamic_game import Game, GameSchema
from app.models.navy.dynamic_ship import DynamicShip
from app.models.navy.start_game_request import StartGameRequest
from app.navy.navy_constants import PATH_TO_START
from app.navy.services.action_service import action_service
from flask import Response

from . import navy

game_schema = GameSchema()


@navy.post("/create")
@token_auth.login_required
def create_game():
    id_game = add_game(request.json["id_user_1"])
    json_resp = read_data(PATH_TO_START)

    json_resp["game_id"] = id_game
    return jsonify(json_resp)


@navy.post("/start")
@token_auth.login_required
def start_game():
    try:
        data = StartGameRequest().load(request.json)
        game_id = data["game_id"]
        add_ship(data)
        game_one = get_game(game_id)
        return jsonify(game_schema.dump(game_one))
    except ValidationError as err:
        return jsonify(err.messages), 400


@navy.post("/action")
def action():
    try:
        data = action_service.validate_request(request.json)
        action_service.add(data)
        return NavyResponse(201,data=data, message="Action added").to_json(), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
