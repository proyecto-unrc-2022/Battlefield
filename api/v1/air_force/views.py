import json
import re
from webbrowser import get

from flask import Blueprint, Response, jsonify, request
from sqlalchemy import insert, select, update

from api import token_auth
from app import db
from app.daos.airforce.plane_dao import add_machine_gun, add_plane
from app.daos.airforce.plane_dao import get_plane as get_plane_dao
from app.daos.airforce.plane_dao import get_projectile
from app.daos.airforce.plane_dao import get_machine_gun
from app.daos.airforce.plane_dao import update_course as update_course_dao
from app.models.airforce.air_force_game import AirForceGame, battlefield
from app.models.airforce.plane import Plane, PlaneSchema, ProjectileSchema
from app.models.user import User


from . import air_force

users_bp = Blueprint("airforce", __name__, url_prefix="/airforce")

plane_schema = PlaneSchema()
proj_schema = ProjectileSchema()


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


@air_force.route("/updateCourse", methods=["PUT"])
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


@air_force.route("/plane_position", methods=["PUT"])
def choice_plane_and_position():

    player = request.json["player"]
    flying_object = request.json["plane"]
    x = request.json["x"]
    y = request.json["y"]
    course = request.json["course"]

    plane = Plane.query.filter_by(id=flying_object).first()

    try:
        obj = battlefield.add_new_plane(player, plane, int(x), int(y), int(course))
    except:
        return Response(status=400)
    return jsonify(obj.to_dict())


@air_force.route("/projectile", methods=["POST"])
def create_projectile():

    player = request.json["player"]
    flying_object = request.json["projectile"]
    x = request.json["x"]
    y = request.json["y"]
    course = request.json["course"]

    proj = get_projectile(projectile_id=flying_object)
    obj = battlefield.add_new_projectile(
        player,
        proj,
        int(x),
        int(y),
        int(course),
    )
    return jsonify(obj.to_dict())


@air_force.route("/update_location_projectile", methods=["PUT"])
def update_location_projectile():

    projectile = request.json["projectile"]
    player = request.json["player"]

    move = battlefield.move_projectile(projectile, player)

    return jsonify(move.to_dict())


@air_force.route("/attack")
@token_auth.login_required
def attack():
    return {"result": "booom!!!"}


@air_force.route("/<player>/<course>", methods=["PUT"])
def fligth(player, course):
    AirForceGame.battlefield.fligth(player, int(course))
    return Response(status=201)


@air_force.route("/machine_gun", methods=["POST"])
def create_machine_gun():
    damage_1 = request.json["damage_1"]
    damage_2 = request.json["damage_2"]
    damage_3 = request.json["damage_3"]
    
    m = add_machine_gun(damage_1, damage_2, damage_3)
    return jsonify(plane_schema.dump(m))