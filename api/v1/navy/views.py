from flask import Response, jsonify, request
from marshmallow import ValidationError

from api import token_auth
from app.navy.daos.missile_type_dao import missile_type_dao
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.dtos.navy_game_dto import NavyGameDTO
from app.navy.services.action_service import action_service
from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.ship_service import ship_service
from app.navy.utils.navy_response import NavyResponse
from app.navy.utils.navy_utils import utils

from . import navy


@navy.post("/actions")
@token_auth.login_required
def action():
    try:
        request.json["user_id"] = token_auth.current_user().id
        data = action_service.validate_request(request.json)
        action_service.add(data)
        if navy_game_service.should_update(data["navy_game_id"]):
            navy_game_service.play_round(data["navy_game_id"])
        return (
            NavyResponse(201, data=request.json, message="Action added").to_json(),
            201,
        )
    except ValidationError as err:
        return jsonify(err.messages), 400


@navy.post("/ships")
@token_auth.login_required
def new_ship():
    try:
        request.json["user_id"] = token_auth.current_user().id
        data = ship_service.validate_request(request.json)
        ship_service.add(data)
        return NavyResponse(201, data=data, message="Ship added").to_json(), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@navy.post("/navy_games")
@token_auth.login_required
def new_navy_game():
    try:
        validated_data = navy_game_service.validate_post_request(request.json)
        created_game = navy_game_service.add(validated_data)
        return (
            NavyResponse(
                201, data=NavyGameDTO().dump(created_game), message="Game created."
            ).to_json(),
            201,
        )
    except ValidationError as err:
        return jsonify(err.messages), 400


@navy.get("/navy_games")
@token_auth.login_required
def get_navy_games():
    user_id = request.args.get("user_id")
    if user_id:
        games = navy_game_service.get_all(user_id)
    else:
        games = navy_game_service.get_all()
    json_games = list(map(lambda game: NavyGameDTO().dump(game), games))
    return NavyResponse(status=200, data=json_games, message="Ok").to_json(), 200


@navy.get("/navy_games/<id>")
@token_auth.login_required
def get_navy_game(id):
    game = navy_game_service.get_by_id(id)
    return (
        NavyResponse(status=200, data=NavyGameDTO().dump(game), message="Ok").to_json(),
        200,
    )


@navy.patch("/navy_games/<id>")
@token_auth.login_required
def update_navy_game(id):
    try:
        validated_data = navy_game_service.validate_patch_request(request.json)
        game = navy_game_service.join(validated_data, id)
        return (
            NavyResponse(
                200, data=NavyGameDTO().dump(game), message="Game updated."
            ).to_json(),
            200,
        )
    except ValidationError as err:
        return jsonify(err.messages), 400


@navy.delete("/navy_games/<id>")
@token_auth.login_required
def delete_navy_game(id):
    deleted_game = navy_game_service.delete(id)
    return (
        NavyResponse(
            status=200, data=NavyGameDTO().dump(deleted_game), message="Game deleted."
        ).to_json(),
        200,
    )


@navy.get("/navy_active_games")
@token_auth.login_required
def get_navy_active_games():
    games = navy_game_service.get_active_games()
    json_games = list(map(lambda game: NavyGameDTO().dump(game), games))
    return NavyResponse(status=200, data=json_games, message="Ok").to_json(), 200


@navy.get("/ship_types")
@token_auth.login_required
def ship_types():
    ships = ship_type_dao.SHIP_TYPES
    return NavyResponse(status=200, data=ships, message="Ok").to_json(), 200


@navy.get("/missile_types")
@token_auth.login_required
def missile_types():
    missiles = missile_type_dao.MISSILE_TYPES
    return NavyResponse(status=200, data=missiles, message="Ok").to_json(), 200
