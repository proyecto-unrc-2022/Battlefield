from flask import Response, request

from api import token_auth, verify_token
from app import db
from app.daos.user_dao import add_user, get_user_by_id
from app.underwater.command import (
    AdvanceTorpedo,
    RotateAndAdvance,
    RotateAndAttack,
    SendRadarPulse,
)
from app.underwater.daos.session_dao import session_dao
from app.underwater.daos.submarine_dao import submarine_dao
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.models.under_game import UnderGame

from . import underwater

# from app.underwater.under_dtos import game_dto


@underwater.post("/reset")
def reset():
    db.drop_all()
    db.create_all()

    add_user("joel", "joel", "joel@mail")
    add_user("blito", "blito", "blito@mail")

    return Response("{'message': 'success'}", status=200)


@underwater.get("/game/<int:session_id>")
@token_auth.login_required
def get_game_state(session_id):
    token = request.headers["token"]
    player = verify_token(token)
    session = session_dao.get_by_id(session_id)
    return session.get_visible_state(player)


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
    new_session = session_dao.start_session_for(game)

    return "{'session_id': '%d'}" % new_session.id


@underwater.post("/game/<int:session_id>/join")
def join_game(session_id):
    data = request.form.to_dict()

    visitor = get_user_by_id(data["visitor_id"])
    game_session = session_dao.get_by_id(session_id)

    if game_session.visitor is not None:
        return Response("{'error':'game does not have an available slot'}", status=409)

    if visitor is game_session.host:
        return Response(
            "{'error':'you cannot be a visitor to your own game'}", status=409
        )

    game_session.add_visitor(visitor)

    session_dao.save(game_session)
    return "{'success': 'user joined the game'}"


@underwater.post("/game/<int:session_id>/<int:player_id>/choose_submarine")
def choose_submarine(session_id, player_id):
    data = request.form.to_dict()
    for key in data.keys():
        data[key] = int(data[key])

    session = session_dao.get_by_id(session_id)
    player = get_user_by_id(player_id)

    if not session:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    try:
        sub = session.game.add_submarine(
            player,
            data["submarine_id"],
            data["x_position"],
            data["y_position"],
            data["direction"],
        )
        submarine_dao.save(sub)
    except Exception as e:
        return Response("{'error': %s}" % str(e), status=409)
    session_dao.save(session)

    return "{'success': submarine placed}"


@underwater.post("/game/<int:session_id>/<int:player_id>/rotate_and_advance")
def rotate_and_advance(session_id, player_id):
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    session = session_dao.get_by_id(session_id)
    player = get_user_by_id(player_id)

    if not session:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    submarine = player.submarine
    direction = data["direction"]
    steps = data["steps"]

    if direction == (submarine.direction + 4) % 8:
        return Response("{'error':'submarines cant rotate 180 degrees'}", status=409)

    if session.current_turn_player() is not player:
        return Response("{'error': 'not your turn'}", status=409)

    c = RotateAndAdvance(session.game, submarine, direction=direction, steps=steps)
    session.add_command(c)
    print(c.name)

    update_session(session)
    return "{'success': 'command enqueued'}"


@underwater.post("/game/<int:session_id>/<int:player_id>/rotate_and_attack")
def rotate_and_attack(session_id, player_id):
    data = request.form.to_dict()
    for key in data:
        data[key] = int(data[key])

    session = session_dao.get_by_id(session_id)
    player = get_user_by_id(player_id)

    if not session:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    submarine = player.submarine
    direction = data["direction"]

    if direction == (submarine.direction + 4) % 8:
        return Response("{'error':'submarines cant rotate 180 degrees'}", status=409)

    if session.current_turn_player() is not player:
        return Response("{'error': 'not your turn'}", status=409)

    session.add_command(RotateAndAttack(session.game, submarine, direction=direction))

    update_session(session)
    return "{'success': 'command enqueued'}"


@underwater.post("/game/<int:session_id>/<int:player_id>/send_radar_pulse")
def send_radar_pulse(session_id, player_id):
    session = session_dao.get_by_id(session_id)
    player = get_user_by_id(player_id)

    if not session:
        return Response("{'error':'game not found'}", status=404)
    if not player:
        return Response("{'error':'player not found'}", status=404)

    submarine = player.submarine

    session.add_command(SendRadarPulse(session.game, submarine))
    update_session(session)
    return "{'success': 'command enqueued'}"


@underwater.get("/game/submarine_options")
def get_options():
    return UnderGame.get_options()


def update_session(session):
    if session.everyone_moved():
        session.execute_commands()
        session.invert_order()
        for torpedo in session.game.torpedos:
            session.add_command(AdvanceTorpedo(torpedo))
    else:
        session.next_turn()
    session_dao.save(session)
