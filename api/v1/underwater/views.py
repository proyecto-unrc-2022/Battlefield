import json

from flask import request

from api import token_auth
from app.daos.underwater.uw_game_dao import create_game

from . import underwater


@underwater.get("/new_game")
# @token_auth.login_required
def new_game():
    ng = create_game(request.args.get("host_id"))
    return ng.__repr__()


@underwater.get("/get_options")
def get_options():
    options_json = open("app/models/underwater/options.json")
    options = json.load(options_json)
    return options
