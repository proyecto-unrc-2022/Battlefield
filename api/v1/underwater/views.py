import json
from os import stat_result

from flask import Response, jsonify, request

from api import token_auth
from app import db
from app.models.user import User
from app.underwater.daos.submarine_dao import SubmarineDAO
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.under_dtos import game_dto
from app.underwater.models.under_game import UnderGame

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

    new_game = game_dao.create(request.args.get("host_id"), height=height, width=width)
    return game_dto.dump(new_game)


@underwater.get("/get_options")
def get_options():
    return UnderGameDAO.get_options()


@underwater.get("/join_game")
def join_game():
    try:
        game_dao = UnderGameDAO.get(request.args.get("game_id"))
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

    submarines = json.load(open("app/underwater/options.json"))

    try:
        game_dao = UnderGameDAO.get(game_id)
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
        submarine_dao = SubmarineDAO.get(submarine_id)
    except Exception:
        return Response("{'error':'submarine not found'}", status="404")

    if submarine_dao.is_placed():
        return Response("{'error':'submarine is already placed'}", status="409")

    try:
        game_dao = UnderGameDAO.get(submarine_dao.get_game().id)
        game_dao.place(submarine_dao.submarine, x_coord, y_coord, direction)
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status="409")

    return Response("{'success':'submarine placed'}", status="200")
