import json
from os import stat_result

from flask import Response, jsonify, request

from api import token_auth
from app import db
from app.daos.underwater.submarine_dao import SubmarineDao
from app.daos.underwater.under_game_dao import UnderGameDao
from app.models.underwater.under_models import UnderGame
from app.models.user import User

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

    ng_dao = UnderGameDao.create(request.args.get("host_id"), height, width)
    return ng_dao.jsonify()


@underwater.get("/get_options")
def get_options():
    return UnderGameDao.get_options()


@underwater.get("/join_game")
def join_game():
    try:
        game_dao = UnderGameDao.get(request.args.get("game_id"))
    except Exception as e:
        return Response("{'error':%s" % str(e), status="404")

    visitor_id = int(request.args.get("visitor_id"))

    if game_dao.get_visitor():
        return Response(
            "{'error':'game does not have an available slot'}", status="409"
        )

    if visitor_id == game_dao.get_host().id:
        return Response("{'error':'you can not join to your game'}", status="409")

    game_dao.update(visitor_id=visitor_id)

    return game_dao.jsonify()


@underwater.post("/choose_submarine")
def choose_submarine():
    game_id = int(request.form["game_id"])
    player_id = int(request.form["player_id"])
    submarine_id = request.form["submarine_id"]

    submarines = json.load(open("app/models/underwater/options.json"))

    try:
        game_dao = UnderGameDao.get(game_id)
    except Exception:
        return Response("{'error':'game not found'}", status="404")

    try:
        game_dao.add_submarine(player_id, submarine_id)
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status="409")

    return game_dao.jsonify()


# Takes submarine_id, x_coord, y_coord, direction
@underwater.post("/place_submarine")
def place_submarine():
    submarine_id = int(request.form["submarine_id"])
    x_coord = int(request.form["x_coord"])
    y_coord = int(request.form["y_coord"])
    direction = int(request.form["direction"])

    try:
        submarine_dao = SubmarineDao.get(submarine_id)
    except Exception:
        return Response("{'error':'submarine not found'}", status="404")

    if submarine_dao.is_placed():
        return Response("{'error':'submarine is already placed'}", status="409")

    try:
        game_dao = UnderGameDao.get(submarine_dao.get_game().id)
        game_dao.place(submarine_dao.submarine, x_coord, y_coord, direction)
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status="409")

    return Response("{'success':'submarine placed'}", status="200")
