from flask import Blueprint, Response, jsonify, request
from sqlalchemy import insert, select, update

from api import token_auth
from app import db
from app.daos.airforce.plane_dao import add_plane
from app.daos.airforce.plane_dao import get_plane as get_plane_dao
from app.daos.airforce.plane_dao import update_direction as update_direction_dao
from app.models.airforce.plane import Plane, PlaneSchema

from . import air_force

users_bp = Blueprint("airforce", __name__, url_prefix="/airforce")

plane_schema = PlaneSchema()


@air_force.route("/<plane_id>", methods=["GET"])
def get_plane(plane_id):
    plane = get_plane_dao(plane_id)
    return jsonify(plane_schema.dump(plane))


@air_force.route("/newplane", methods=["POST"])
def put_plane():
    name = request.json["name"]
    size = request.json["size"]
    speed = request.json["speed"]
    health = request.json["health"]
    direct_of_plane = request.json["direct_of_plane"]
    coor_x = request.json["coor_x"]
    coor_y = request.json["coor_y"]
    p = add_plane(name, size, speed, health, direct_of_plane, coor_x, coor_y)
    return jsonify(plane_schema.dump(p))


@air_force.route("/updatedirection", methods=["PUT"])
def update_direction():
    id_plane = request.json["id"]
    new_direction = request.json["direct_of_plane"]
    old_direction = Plane.query.filter_by(id=id_plane).first().direct_of_plane
    if (
        old_direction == "north"
        and new_direction == "south"
        or old_direction == "south"
        and new_direction == "north"
    ):
        return Response(status=404)
    elif (
        old_direction == "east"
        and new_direction == "west"
        or old_direction == "west"
        and new_direction == "east"
    ):
        return Response(status=404)
    else:
        p = update_direction_dao(id_plane, new_direction)
        return Response(status=201)  # or jsonify(plane_schema.dump(p))


@air_force.route("/attack")
@token_auth.login_required
def attack():
    return {"result": "booom!!!"}


@air_force.route("/flight")
def fligth():
    return {"a": "a"}
