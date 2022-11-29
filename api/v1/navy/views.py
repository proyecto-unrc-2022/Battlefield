from flask import jsonify, request
from flask_socketio import join_room, leave_room
from marshmallow import ValidationError

from api import token_auth
from app import io
from app.navy.daos.missile_type_dao import missile_type_dao
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.dtos.navy_game_dto import NavyGameDTO
from app.navy.dtos.navy_game_spectate_dto import NavyGameSpectateDTO
from app.navy.dtos.navy_game_state_dto import NavyGameStateDTO
from app.navy.services.action_service import action_service
from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.ship_service import ship_service
from app.navy.services.spectate_service import spectate_service
from app.navy.utils.navy_response import NavyResponse
from app.navy.utils.navy_utils import utils
from app.navy.validators.action_request_validator import ActionRequestValidator
from app.navy.validators.navy_game_patch_validator import NavyGamePatchValidator
from app.navy.validators.ship_request_validator import ShipRequestValidator
from app.navy.validators.spectate_validator import SpectateValidator

from . import navy


@navy.post("/actions")
@token_auth.login_required
def new_action():
    try:
        request.json["user_id"] = utils.get_user_id_from_header(
            request.headers["Authorization"]
        )
        validated_data = ActionRequestValidator().load(request.json)
        action_service.add(validated_data)
        return (
            NavyResponse(201, data=request.json, message="Action added").to_json(),
            201,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.post("/ships")
@token_auth.login_required
def new_ship():
    try:
        request.json["user_id"] = utils.get_user_id_from_header(
            request.headers["Authorization"]
        )
        validated_data = ShipRequestValidator().load(request.json)
        ship_service.add(validated_data)
        return (
            NavyResponse(201, data=validated_data, message="Ship added").to_json(),
            201,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.post("/navy_games")
@token_auth.login_required
def new_navy_game():
    try:
        user1_id = utils.get_user_id_from_header(request.headers["Authorization"])
        created_game = navy_game_service.add({"user1_id": user1_id})
        return (
            NavyResponse(
                201, data=NavyGameDTO().dump(created_game), message="Game created."
            ).to_json(),
            201,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.get("/navy_games")
@token_auth.login_required
def get_navy_games():
    games = navy_game_service.get_all()
    json_games = list(map(lambda game: NavyGameDTO().dump(game), games))
    return NavyResponse(status=200, data=json_games, message="Ok").to_json(), 200


@navy.get("/navy_games/<int:id>")
@token_auth.login_required
def get_navy_game(id):
    from app.navy.validators.navy_game_get_validator import NavyGameGetValidator

    try:
        user_id = utils.get_user_id_from_header(request.headers["Authorization"])
        NavyGameGetValidator().load({"navy_game_id": id, "user_id": user_id})
        return (
            NavyResponse(
                status=200, data=NavyGameStateDTO(id, user_id).dump(), message="Ok"
            ).to_json(),
            200,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.get("/spectate/<int:id>")
@token_auth.login_required
def spectate_navy_game(id):
    try:
        round = request.args.get("round")
        round = int(round) if round else 0
        SpectateValidator().load({"navy_game_id": id, "round": round})
        return (
            NavyResponse(
                status=200, data=NavyGameSpectateDTO(id, round).dump(), message="Ok"
            ).to_json(),
            200,
        )
    except ValidationError as err:
        return jsonify(err.messages), 400


@navy.patch("/navy_games/<int:id>")
@token_auth.login_required
def update_navy_game(id):
    try:
        user2_id = utils.get_user_id_from_header(request.headers["Authorization"])
        validated_data = NavyGamePatchValidator().load(
            {"user2_id": user2_id, "game_id": id}
        )
        game = navy_game_service.join(validated_data)
        return (
            NavyResponse(
                200, data=NavyGameDTO().dump(game), message="Game updated."
            ).to_json(),
            200,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


@navy.delete("/navy_games/<int:id>")
@token_auth.login_required
def delete_navy_game(id):
    try:
        from app.navy.validators.delete_game_validator import DeleteGameValidator

        user_id = utils.get_user_id_from_header(request.headers["Authorization"])
        validated_data = DeleteGameValidator().load({"game_id": id, "user_id": user_id})
        deleted_game = navy_game_service.delete(validated_data["game_id"])
        return (
            NavyResponse(
                200, data=NavyGameDTO().dump(deleted_game), message="Game deleted."
            ).to_json(),
            200,
        )
    except ValidationError as err:
        return NavyResponse(400, message=err.messages).to_json(), 400


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


@io.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)


@io.on("leave")
def on_leave(data):
    room = data["room"]
    leave_room(room)


@io.on("message")
def handle_message(data):
    response = {"body": data["body"], "user": data["user"]}
    io.send(response, to=data["room"])
