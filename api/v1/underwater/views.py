import json
from os import stat_result

from flask import Response, jsonify, request

from api import token_auth
from app.daos.user_dao import get_user_by_id
from app.models.user import User
from app.underwater import boards
from app.underwater.command import AdvanceTorpedo, RotateAndAdvance, RotateAndAttack
from app.underwater.daos.submarine_dao import SubmarineDAO, submarine_dao
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.models.under_game import UnderGame
from app.underwater.session import sessions
from app.underwater.session.under_game_session import UnderGameSession
from app.underwater.under_dtos import game_dto

from . import underwater


@underwater.get("/new_game")
# @token_auth.login_required
def new_game():
    if not request.args.get("host_id"):
        return Response("{'error':'must pass a host id'", status="409")

    host = get_user_by_id(request.args.get("host_id"))

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


@underwater.get("/join_game")
def join_game():
    visitor_id = int(request.args.get("visitor_id"))
    visitor = get_user_by_id(visitor_id)
    game = game_dao.get_by_id(request.args.get("game_id"))
    game_session = sessions[game.id]

    if game.visitor_id is not None:
        return Response("{'error':'game does not have an available slot'}", status=409)

    if visitor_id == game.host_id:
        return Response(
            "{'error':'you cannot be a visitor to your own game'}", status=409
        )

    game.visitor_id = visitor_id

    game_session.add_player(visitor)

    game_dao.save(game)
    return game_dto.dumps(game)


@underwater.post("/choose_submarine")
def choose_submarine():
    # data = request.json
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    game_id = data["game_id"]
    player_id = data["player_id"]
    submarine_id = data["submarine_id"]
    x_position = data["x_position"]
    y_position = data["y_position"]
    direction = data["direction"]
    game = game_dao.get_by_id(game_id)
    player = get_user_by_id(player_id)

    if not game:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    try:
        game.add_submarine(player, submarine_id, x_position, y_position, direction)
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status=409)

    game_dao.save(game)
    return game_dto.dump(game)


@underwater.post("/rotate_and_advance")
def rotate_and_advance():
    # data = request.json
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    game = game_dao.get_by_id(data["game_id"])
    submarine = submarine_dao.get_by_id(data["submarine_id"])
    direction = data["direction"]
    steps = data["steps"]
    game_session = sessions[game.id]

    if game_session.current_turn_player() is not submarine.player:
        return Response("{'error': 'not your turn'}", status=409)

    game_session.add_command(
        RotateAndAdvance(game, submarine, direction=direction, steps=steps)
    )
    update_game(game)

    game_dao.save(game)
    return game_dto.dump(game)


@underwater.post("/rotate_and_attack")
def rotate_and_attack():
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    game = game_dao.get_by_id(data["game_id"])
    submarine = submarine_dao.get_by_id(data["submarine_id"])
    direction = data["direction"]
    game_session = sessions[game.id]

    if game_session.current_turn_player() is not submarine.player:
        return Response("{'error': 'not your turn'}", status=409)

    game_session.add_command(RotateAndAttack(game, submarine, direction=direction))
    update_game(game)

    game_dao.save(game)
    return game_dto.dump(game)


@underwater.get("/get_options")
def get_options():
    return UnderGame.get_options()


def update_game(game):
    game_session = sessions[game.id]
    if game_session.everyone_moved():
        game_session.execute_commands()
        game_session.invert_order()
        for torpedo in game.get_torpedos():
            game_session.add_command(AdvanceTorpedo(torpedo))
    else:
        game_session.next_turn()
