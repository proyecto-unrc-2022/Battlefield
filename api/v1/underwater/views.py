import json
from os import stat_result

from flask import Response, jsonify, request

from api import token_auth
from app.daos.user_dao import get_user_by_id
from app.models.user import User
from app.underwater.daos.submarine_dao import SubmarineDAO, submarine_dao
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.models.under_game import UnderGame
from app.underwater.under_dtos import game_dto

from . import underwater


@underwater.get("/new_game")
# @token_auth.login_required
def new_game():
    if not request.args.get("host_id"):
        return Response("{'error':'must pass a host id'", status="409")

    height = 10
    width = 20
    if request.args.get("height"):
        height = request.args.get("height")
    if request.args.get("width"):
        width = request.args.get("width")

    try:
        new_game = game_dao.create(
            request.args.get("host_id"), height=height, width=width
        )
    except Exception as e:
        return Response("{'error':%s}" % str(e), status=409)
    return game_dto.dump(new_game)


@underwater.get("/get_options")
def get_options():
    return UnderGame.get_options()


@underwater.get("/join_game")
def join_game():
    visitor_id = int(request.args.get("visitor_id"))
    game = game_dao.get_by_id(request.args.get("game_id"))

    if game.visitor_id is not None:
        return Response("{'error':'game does not have an available slot'}", status=409)

    if visitor_id == game.host_id:
        return Response(
            "{'error':'you cannot be a visitor to your own game'}", status=409
        )

    game.visitor_id = visitor_id

    game_dao.save(game)
    return game_dto.dumps(game)


@underwater.post("/choose_submarine")
def choose_submarine():
    game_id = request.form.get("game_id", type=int)
    player_id = request.form.get("player_id", type=int)
    submarine_id = request.form.get("submarine_id", type=int)
    x_position = request.form.get("x_position", type=int)
    y_position = request.form.get("y_position", type=int)
    direction = request.form.get("direction", type=int)
    game = game_dao.get_by_id(game_id)
    player = get_user_by_id(player_id)

    if not game:
        return Response("{'error':'game not found'}", status="404")
    if not player:
        return Response("{'error':'player not found'}", status="404")

    try:
        game.add_submarine(player, submarine_id, x_position, y_position, direction)
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status="409")

    game_dao.save(game)
    return game_dto.dump(game)


@underwater.post("/rotate_and_advance")
def rotate_and_advance():
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    game = game_dao.get_by_id(data["game_id"])
    submarine = submarine_dao.get_by_id(data["submarine_id"])
    game.rotate_object(submarine, data["direction"])
    game.advance_object(submarine, data["steps"])

    game_dao.save(game)
    return game_dto.dump(game)


@underwater.post("/rotate_and_attack")
def rotate_and_attack():
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    game = game_dao.get_by_id(data["game_id"])
    submarine = submarine_dao.get_by_id(data["submarine_id"])
    game.rotate_object(submarine, data["direction"])
    game.attack(submarine)

    game_dao.save(game)
    return game_dto.dump(game)
