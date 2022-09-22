from flask import jsonify, request

from app import db
from app.daos.navy.game_dao import add_game
from app.models.navy.dynamic_navy_models import Game, DynamicShip, DynamicMissile, GameSchema
from app.navy.navy_constants import PATH_TO_START
from app.navy.navy_game_control import NavyGameControl


from . import navy
game_schema = GameSchema()


@navy.post("/create")
def create_game():
    id_game = add_game(request.json["id_user_1"])
    json_resp = NavyGameControl.read_data(PATH_TO_START)
    json_resp["game_id"] = id_game
    return jsonify(json_resp)


@navy.post("/start")
def start_game():
    game_id = request.json["game_id"]
    dynamicShip = DynamicShip(
        id_game=game_id,
        id_user=request.json["id_user_1"],
        hp=request.json["hp"],
        direction=request.json["direction"],
        pos_x=request.json["pos_x"],
        pos_y=request.json["pos_y"],
        ship_type=request.json["ship_type"],
    )
    db.session.add(dynamicShip)
    db.session.commit()
    game_one = Game.query.filter_by(id=game_id).first()
    return jsonify(game_schema.dump(game_one))
    