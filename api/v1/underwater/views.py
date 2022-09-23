import json

from flask import Response, jsonify, request

from api import token_auth
from app import db
from app.daos.underwater.uw_game_dao import create_game
from app.models.underwater.uw_game import UnderGame, UnderGameSchema
from app.models.user import User

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


@underwater.get("/join_game")
def join_game():
    game = (
        db.session.query(UnderGame)
        .where(UnderGame.id == request.args.get("game_id"))
        .one_or_none()
    )
    visitor_id = request.args.get("visitor_id")

    if not game:
        return Response("{'error':'game not found'}", status_code=404)
    if game.visitor_id:
        return Response(
            "{'error':'game does not have an available slot'}", status_code=409
        )
    if visitor_id == game.host_id:
        return Response("{'error':'you can not join to your game'}", status_code=409)

    game.visitor_id = visitor_id
    db.session.commit()
    return jsonify(under_game_schema.dump(game))
