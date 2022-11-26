import json

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
from app.underwater.game_state import GameState
from app.underwater.message_announcer import MessageAnnouncer, announcers, format_sse
from app.underwater.models.under_game import UnderGame

from . import underwater

# from app.underwater.under_dtos import game_dto


@underwater.get("/game/<int:session_id>/listen")
def listen(session_id):

    announcer = announcers[session_id]

    def stream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield msg

    return Response(stream(), mimetype="text/event-stream")


@underwater.post("/reset")
def reset():
    db.drop_all()
    db.create_all()

    add_user("joel", "joel", "joel@mail")
    add_user("blito", "blito", "blito@mail")

    return Response('{"message": "success"}', status=200)


@underwater.get("/games")
@token_auth.login_required
def get_all_games():
    retDict = {}
    sessions = session_dao.get_all()

    for session in sessions:
        retDict.update({session.id: session.to_dict()})

    return retDict


@underwater.get("/game/<int:session_id>")
@token_auth.login_required
def get_game_state(session_id):
    token = get_token(request)
    player = get_player_from(token)
    session = session_dao.get_by_id(session_id)

    if not player:
        return Response('{"error": "could not find a player"}', status=404)
    if not session:
        return Response('{"error": "could not find a session"}', status=404)

    if not session.has_player(player):
        return Response('{"error": "invalid session"}')

    return session.get_visible_state(player)


@underwater.post("/game/new")
@token_auth.login_required
def new_game():
    data = request.form.to_dict()
    token = get_token(request)
    host = get_player_from(token)

    if not host:
        return Response('{"error": "could not find a player"}', status=404)
    if host.under_game_host or host.under_game_visitor:
        return Response('{"error": "player is in another game"}', status=409)

    height = 10
    width = 20
    if "height" in data.keys():
        height = data["height"]
    if "width" in data.keys():
        width = data["width"]

    game = game_dao.create(host=host, width=width, height=height)
    new_session = session_dao.start_session_for(game)

    print(f"Creating announcer for game session {new_session.id}")
    announcers.update({new_session.id: MessageAnnouncer()})

    return json.dumps({"game_id": new_session.id})


@underwater.post("/game/<int:session_id>/join")
@token_auth.login_required
def join_game(session_id):
    token = get_token(request)
    visitor = get_player_from(token)
    game_session = session_dao.get_by_id(session_id)

    if not visitor:
        return Response('{"error": "could not find a player"}', status=409)
    if game_session.visitor is not None:
        return Response('{"error":"game does not have an available slot"}', status=409)
    if visitor is game_session.host:
        return Response(
            '{"error":"you cannot be a visitor to your own game"}', status=409
        )

    game_session.add_visitor(visitor)

    msg = format_sse(data=json.dumps({"message": "joined"}))
    announcers[session_id].announce(msg)

    session_dao.save(game_session)
    return '{"success": "user joined the game"}'


@underwater.post("/game/<int:session_id>/delete")
def delete_game(session_id):
    session_dao.delete(session_id)
    return '{"success": "game deleted"}'


@underwater.post("/game/<int:session_id>/choose_submarine")
@token_auth.login_required
def choose_submarine(session_id):
    print(request.is_json)
    data = request.get_json()

    token = get_token(request)
    player = get_player_from(token)
    session = session_dao.get_by_id(session_id)

    if not session:
        return Response('{"error":"game not found"}', status=404)
    if not player:
        return Response('{"error":"player not found"}', status=404)

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
        return Response('{"error": "%s"}' % str(e), status=409)
    session_dao.save(session)

    msg = format_sse(data=json.dumps({"message": "submarine placed"}))
    announcers[session_id].announce(msg)

    return '{"success": "submarine placed"}'


@underwater.post("/game/<int:session_id>/rotate_and_advance")
@token_auth.login_required
def rotate_and_advance(session_id):
    data = request.json

    token = get_token(request)
    player = get_player_from(token)
    session = session_dao.get_by_id(session_id)

    if not session:
        return Response('{"error":"game not found"}', status=404)
    if not player:
        return Response('{"error":"player not found"}', status=404)

    submarine = player.submarine
    direction = data["direction"]
    steps = data["steps"]

    if direction == (submarine.direction + 4) % 8:
        return Response('{"error":"submarines cant rotate 180 degrees"}', status=409)

    if session.current_turn_player() is not player:
        return Response('{"error": "not your turn"}', status=409)

    session.add_command(
        RotateAndAdvance(session.game, submarine, direction=direction, steps=steps)
    )

    update_session(session)
    return '{"success": "command enqueued"}'


@underwater.post("/game/<int:session_id>/rotate_and_attack")
@token_auth.login_required
def rotate_and_attack(session_id):
    data = request.json

    token = get_token(request)
    player = get_player_from(token)
    session = session_dao.get_by_id(session_id)

    if not session:
        return Response('{"error":"game not found"}', status=404)
    if not player:
        return Response('{"error":"player not found"}', status=404)

    submarine = player.submarine
    direction = data["direction"]

    if direction == (submarine.direction + 4) % 8:
        return Response('{"error":"submarines cant rotate 180 degrees"}', status=409)

    if session.current_turn_player() is not player:
        return Response('{"error": "not your turn"}', status=409)

    session.add_command(RotateAndAttack(session.game, submarine, direction=direction))

    update_session(session)
    return '{"success": "command enqueued"}'


@underwater.post("/game/<int:session_id>/send_radar_pulse")
@token_auth.login_required
def send_radar_pulse(session_id):
    token = get_token(request)
    player = get_player_from(token)
    session = session_dao.get_by_id(session_id)

    if not session:
        return Response('{"error":"game not found"}', status=404)
    if not player:
        return Response('{"error":"player not found"}', status=404)

    submarine = player.submarine

    session.add_command(SendRadarPulse(session.game, submarine))
    update_session(session)
    return '{"success": "command enqueued"}'


@underwater.get("/game/submarine_options")
def get_options():
    return UnderGame.get_options()


def update_session(session):
    if session.everyone_moved():
        session.execute_commands()
        session.invert_order()
        for torpedo in session.game.torpedos:
            session.add_command(AdvanceTorpedo(torpedo))

        msg = format_sse(data=json.dumps({"message": "commands executed"}))
        announcers[session.id].announce(msg)
    else:
        session.next_turn()
    session_dao.save(session)

    if session.game.state == GameState.FINISHED:
        msg = format_sse(data=json.dumps({"winner_id": session.game.winner_id}))
        announcers[session.id].announce(msg)


def get_player_from(token):
    try:
        player = verify_token(token)
    except Exception:
        return None
    return player


def get_token(request):
    return request.headers["authorization"].split()[1]  # Trim "Bearer " prefix
