from flask import Response, jsonify, request

from api import token_auth
from app import db
from app.daos.user_dao import add_user, get_user_by_id
from app.models.user import User
from app.underwater import boards
from app.underwater.command import AdvanceTorpedo, RotateAndAdvance, RotateAndAttack
from app.underwater.daos.submarine_dao import SubmarineDAO, submarine_dao
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.models.under_game import UnderGame
from app.underwater.session import sessions
from app.underwater.session.under_game_session import UnderGameSession

from . import underwater

# from app.underwater.under_dtos import game_dto


@underwater.post("/reset")
def reset():
    db.drop_all()
    db.create_all()

    add_user("joel", "joel", "joel@mail")
    add_user("blito", "blito", "blito@mail")

    return Response("{'message': 'success'}", status=200)


@underwater.get("/game/<int:game_id>")
def get_game_state(game_id):
    game_session = sessions[game_id]
    return game_session.to_dict()


@underwater.post("/game/new")
# @token_auth.login_required
def new_game():
    data = request.form.to_dict()

    host = get_user_by_id(data["host_id"])

    if host.under_game_host or host.under_game_visitor:
        return Response("{'error': 'player is in another game'}", status=409)

    height = 10
    width = 20
    if "height" in data.keys():
        height = data["height"]
    if "width" in data.keys():
        width = data["width"]

    game = game_dao.create(host=host, width=width, height=height)
    new_session = UnderGameSession.start_session_for(game)
    sessions.update({new_session.id: new_session})

    return "{'game_id': '%d'}" % game.id


@underwater.post("/game/<int:game_id>/join")
def join_game(game_id):
    data = request.form.to_dict()

    visitor = get_user_by_id(data["visitor_id"])
    game = game_dao.get_by_id(game_id)

    if game.visitor is not None:
        return Response("{'error':'game does not have an available slot'}", status=409)

    if visitor is game.host:
        return Response(
            "{'error':'you cannot be a visitor to your own game'}", status=409
        )

    game.visitor = visitor

    game_dao.save(game)
    return "{'success': 'user joined the game'}"


@underwater.post("/game/<int:game_id>/<int:player_id>/choose_submarine")
def choose_submarine(game_id, player_id):
    data = request.form.to_dict()
    for key in data.keys():
        data[key] = int(data[key])

    game = game_dao.get_by_id(game_id)
    player = get_user_by_id(player_id)

    if not game:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    try:
        sub = game.add_submarine(
            player,
            data["submarine_id"],
            data["x_position"],
            data["y_position"],
            data["direction"],
        )
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status=409)

    return "{'success': submarine placed}"


@underwater.post("/game/<int:game_id>/<int:player_id>/rotate_and_advance")
def rotate_and_advance(game_id, player_id):
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    game = game_dao.get_by_id(game_id)
    player = get_user_by_id(player_id)

    if not game:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    submarine = player.submarine
    direction = data["direction"]
    steps = data["steps"]
    game_session = sessions[game_id]

    if direction == (submarine.direction + 4) % 8:
        return Response("{'error':'submarines cant rotate 180 degrees'}", status=409)

    print("here 1")
    if game_session.current_turn_player() is not player:
        return Response("{'error': 'not your turn'}", status=409)

    game_session.add_command(
        RotateAndAdvance(game, submarine, direction=direction, steps=steps)
    )
    update_game(game)

    game_dao.save(game)
    return game.__repr__()


@underwater.post("/game/<int:game_id>/<int:player_id>/rotate_and_attack")
def rotate_and_attack(game_id, player_id):
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    game = game_dao.get_by_id(game_id)
    player = get_user_by_id(player_id)

    if not game:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    submarine = player.submarine
    direction = data["direction"]
    game_session = sessions[game.id]

    if direction == (submarine.direction + 4) % 8:
        return Response("{'error':'submarines cant rotate 180 degrees'}", status=409)

    if game_session.current_turn_player() is not player:
        return Response("{'error': 'not your turn'}", status=409)

    game_session.add_command(RotateAndAttack(game, submarine, direction=direction))
    update_game(game)

    game_dao.save(game)
    return game.__repr__()


@underwater.get("/game/submarine_options")
def get_options():
    return UnderGame.get_options()


def update_game(game):
    game_session = sessions[game.id]
    if game_session.everyone_moved():
        game_session.execute_commands()
        game_session.invert_order()
        for torpedo in game.get_torpedos():
            torpedo.save()
            game_session.add_command(AdvanceTorpedo(torpedo))
    else:
        game_session.next_turn()
