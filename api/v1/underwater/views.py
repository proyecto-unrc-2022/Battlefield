import json
from os import stat_result

from flask import Response, jsonify, request

from api import token_auth
from app import db
from app.daos.underwater.submarine_dao import get_submarine, is_placed
from app.daos.underwater.uw_game_dao import add_submarine, create_game, get_game
from app.daos.underwater.uw_game_dao import get_options as get_options_dao
from app.daos.underwater.uw_game_dao import has_user
from app.daos.underwater.uw_game_dao import place_submarine as place_sub
from app.daos.underwater.uw_game_dao import update_game
from app.models.underwater.under_dtos import UnderGameSchema
from app.models.underwater.under_models import UnderGame
from app.models.user import User

from . import underwater

under_game_schema = UnderGameSchema()


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

    ng = create_game(request.args.get("host_id"), height, width)
    return jsonify(under_game_schema.dump(ng))


@underwater.get("/get_options")
def get_options():
    return get_options_dao()


@underwater.get("/join_game")
def join_game():
    game = get_game(request.args.get("game_id"))
    visitor_id = int(request.args.get("visitor_id"))

    if not game:
        return Response("{'error':'game not found'}", status="404")
    if game.visitor_id:
        return Response(
            "{'error':'game does not have an available slot'}", status="409"
        )
    if visitor_id == game.host_id:
        return Response("{'error':'you can not join to your game'}", status="409")

    game = update_game(game_id=game.id, visitor_id=visitor_id)

    return jsonify(under_game_schema.dump(game))


@underwater.post("/choose_submarine")
def choose_submarine():
    game_id = int(request.form["game_id"])
    player_id = int(request.form["player_id"])
    submarine_id = request.form["submarine_id"]

    submarines = json.load(open("app/models/underwater/options.json"))

    game = get_game(game_id=game_id)
    if not game:
        return Response("{'error':'game not found'}", status="404")

    try:
        add_submarine(game, player_id, submarine_id)
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status="409")

    return jsonify(under_game_schema.dump(game))


# Takes submarine_id, x_coord, y_coord, direction
@underwater.post("/place_submarine")
def place_submarine():
    submarine_id = int(request.form["submarine_id"])
    x_coord = int(request.form["x_coord"])
    y_coord = int(request.form["y_coord"])
    direction = int(request.form["direction"])
    submarine = get_submarine(submarine_id)

    if not submarine:
        return Response("{'error':'submarine not found'}", status="404")
    if is_placed(submarine):
        return Response("{'error':'submarine is already placed'}", status="409")
    try:
        place_sub(submarine, x_coord, y_coord, direction)
    except Exception as e:
        return Response("{'error':'%s'}" % str(e), status="409")

    return Response("{'success':'submarine placed'}", status="200")
