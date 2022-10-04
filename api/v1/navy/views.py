from flask import jsonify, request
from marshmallow import ValidationError

from app import db
from app.daos.navy.dynamic_ship_dao import add_ship
from app.daos.navy.game_dao import add_game, get_game, read_data
from app.models.navy.dynamic_game import Game, GameSchema
from app.models.action_game_request import ActionGameRequest
from app.models.navy.dynamic_ship import DynamicShip
from app.navy.navy_constants import PATH_TO_START

from . import navy

game_schema = GameSchema()



@navy.post("/create")
def create_game():
    id_game = add_game(request.json["id_user_1"])
    json_resp = read_data(PATH_TO_START)

    json_resp["game_id"] = id_game
    return jsonify(json_resp)


@navy.post("/start")
def start_game():
    game_id = request.json["game_id"]
    add_ship(
        game_id,
        request.json["id_user_1"],
        request.json["hp"],
        request.json["direction"],
        request.json["pos_x"],
        request.json["pos_y"],
        request.json["ship_type"],
    )
    game_one = get_game(game_id)
    return jsonify(game_schema.dump(game_one))


@navy.get("/test")
def test():
    game_one = Game.query.filter_by(id=1).first()
    return jsonify(game_schema.dump(game_one))

@navy.post("/action")
def action():
    try:
        data = ActionGameRequest().load(request.json)
        return jsonify(data)
    except ValidationError as err:
        return jsonify(err.messages),400
