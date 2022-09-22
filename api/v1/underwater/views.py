import json

from flask import jsonify, request

from api import token_auth
from app.daos.underwater.uw_game_dao import create_game
from app.models.underwater.uw_game import UnderGame, UnderGameSchema

from . import underwater

under_game_schema = UnderGameSchema()


@underwater.get("/new_game")
# @token_auth.login_required
def new_game():
    ng = create_game(request.args.get("host_id"))
    return jsonify(under_game_schema.dump(ng))


@underwater.get("/get_options")
def get_options():
    options_json = open("app/models/underwater/options.json")
    options = json.load(options_json)
    return options
