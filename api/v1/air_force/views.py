import json
from webbrowser import get

from flask import Blueprint, Response, jsonify, request
from sqlalchemy import insert, select, update

from api import token_auth
from app import db
from app.daos.airforce.plane_dao import add_plane
from app.daos.airforce.plane_dao import get_plane as get_plane_dao
"""from app.daos.airforce.plane_dao import update_course as update_course_dao"""
from app.models.airforce.air_force_game import AirForceGame
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
    p = add_plane(name, size, speed, health)
    return jsonify(plane_schema.dump(p))


"""@air_force.route("/updateCourse", methods=["PUT"])
def update_course():
    id_plane = request.json["id"]
    new_course = request.json["course"]
    old_course = Plane.query.filter_by(id=id_plane).first().course
    if 2 == abs(new_course - old_course):
        return Response(status=400)
    else:
        p = update_course_dao(id_plane, new_course)
        return Response(status=201)  # or jsonify(plane_schema.dump(p))"""


@air_force.route("/<player>", methods=["PUT"])
def join_in_game(player):
    try:
        game = AirForceGame.join_game(new_player=player)
    except:
        return Response(status=400)
    return jsonify(game)


@air_force.route("/attack")
@token_auth.login_required
def attack():
    return {"result": "booom!!!"}


@air_force.route("/flight")
def fligth():
    return {"a": "a"}
