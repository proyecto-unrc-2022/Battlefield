from flask import Blueprint, Response, jsonify, request
from sqlalchemy import insert, select

from api import token_auth
from app import db
from app.daos.airforce.plane_dao import get_plane as get_plane_dao
from app.models.airforce.plane import Plane, PlaneSchema

from . import air_force

users_bp = Blueprint("airforce", __name__, url_prefix="/airforce")

plane_schema = PlaneSchema()


@air_force.route("/<plane_id>", methods=["GET"])
def get_plane(plane_id):
    plane = get_plane_dao(plane_id)
    return jsonify(plane_schema.dump(plane))


@air_force.route("/attack")
@token_auth.login_required
def attack():
    return {"result": "booom!!!"}


@air_force.route("/flight")
def fligth():
    return {"a": "a"}
