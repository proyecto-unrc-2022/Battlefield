from flask import Response, jsonify, request
from marshmallow import ValidationError

from api import token_auth
from app import db
from app.navy.services.action_service import action_service
from app.navy.services.ship_service import ship_service
from app.navy.utils.navy_response import NavyResponse

from . import navy


@navy.post("/actions")
def action():
    try:
        data = action_service.validate_request(request.json)
        action_service.add(data)
        return NavyResponse(201, data=data, message="Action added").to_json(), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@navy.post("/ships")
def new_ship():
    try:
        data = ship_service.validate_request(request.json)
        ship_service.add(data)
        return NavyResponse(201, data=data, message="Ship added").to_json(), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
