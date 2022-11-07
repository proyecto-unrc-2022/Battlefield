import json

from flask import Blueprint, Response, jsonify, request
from flask_cors import CORS

from api import token_auth
from app.daos.airforce.plane_dao import add_machine_gun, add_plane
from app.daos.airforce.plane_dao import get_plane as get_plane_dao
from app.daos.airforce.plane_dao import get_projectile
from app.daos.airforce.plane_dao import update_course as update_course_dao
from app.models.airforce.air_force_game import (
    AirForceGame,
    ChoosePlane,
    GetBattlefieldStatus,
    GetPlayers,
    JoinGame,
    LaunchProjectile,
    MovePlane,
)
from app.models.airforce.plane import Plane, PlaneSchema, ProjectileSchema

from . import air_force

# CORS(air_force, resources={ r'/*': {'origins': '*'}}, supports_credentials=True)

plane_schema = PlaneSchema()
proj_schema = ProjectileSchema()
air_force_game = []  # AirForceGame()#lista de juegos


@air_force.route("/new_game/player/<player>", methods=["POST"])
def new_game(player):
    game = AirForceGame()
    air_force_game.append(game)
    game_id = len(air_force_game) - 1
    command = JoinGame(player=player, air_force_game=game)
    try:
        game.execute(command)
    except:
        return Response(status=400)
    return jsonify({"game_id": game_id})


@air_force.route("/join/game/<id>/player/<player>", methods=["PUT"])
def join_in_game(player, id):
    game = air_force_game[int(id)]
    command = JoinGame(player=player, air_force_game=game)
    try:
        game.execute(command)
    except:
        return Response(status=400)
    command = GetPlayers(game)
    return jsonify(game.execute(command))


@air_force.route("/get_players/game_id/<id>", methods=["GET"])
def get_players(id):
    game = air_force_game[int(id)]
    command = GetPlayers(game)
    return jsonify(game.execute(command))


@air_force.route("/choose_plane", methods=["PUT"])
def choose_plane_and_position():
    game = air_force_game[int(request.json["id"])]
    player = request.json["player"]
    plane = request.json["plane"]
    x = request.json["x"]
    y = request.json["y"]
    course = request.json["course"]

    plane = Plane.query.filter_by(id=plane).first()

    command = ChoosePlane(
        course=course, plane=plane, x=x, y=y, player=player, air_force_game=game
    )
    try:
        dic = game.execute(command)
        return jsonify(dic.to_dict())  # Response(status=201)
    except:
        return Response(status=400)


@air_force.route("game_id/<id>/player/<player>/course/<course>/", methods=["PUT"])
def fligth(id, player, course):
    game = air_force_game[int(id)]
    try:
        game.battlefield.check_course(course, player)
        command = MovePlane(course, player, game)
        game.add_command(command, player)
        return Response(status=201)
    except:
        return Response(status=400)


@air_force.route("get_battlefield_status/game_id/<id>", methods=["GET"])
def get_battlefield_status(id):
    game = air_force_game[int(id)]
    command = GetBattlefieldStatus(game.battlefield)
    obj_list = game.execute(command)
    return jsonify(obj_list)


@air_force.route("/game/plane/<plane_id>", methods=["GET"])
def get_plane(plane_id):
    plane = get_plane_dao(plane_id)
    return jsonify(plane_schema.dump(plane))


@air_force.route("/players/<player>/plane", methods=["GET"])
def get_player_plane(player):
    plane = air_force_game.get_player_plane(player)
    return jsonify(plane)


@air_force.route("/newplane", methods=["POST"])
def put_plane():
    name = request.json["name"]
    size = request.json["size"]
    speed = request.json["speed"]
    health = request.json["health"]
    course = request.json["course"]
    coor_x = request.json["coor_x"]
    coor_y = request.json["coor_y"]
    p = add_plane(name, size, speed, health, course, coor_x, coor_y)
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
        return Response(status=201)  # or jsonify(plane_schema.dump(p))


@air_force.route("/game/<id>/new_projectile/player/<player>", methods=["POST"])
def create_projectile(id, player):
    game = air_force_game[int(id)]
    command = LaunchProjectile(player, game)

    try:
        dic = game.execute(command)
        return jsonify(dic.to_dict())
    except:
        return Response(status=400)


# @air_force.route("/<player_projectile>/<course>", methods=["PUT"])
# def move_projectile(player_projectile, course):
#     move = air_force_game.battlefield.move_projectile(
#         player=int(player_projectile), course=int(course)
#     )
#     return jsonify(move)


@air_force.route("/attack")
# @token_auth.login_required
def attack():
    return {"result": "booom!!!"}


@air_force.route("/machine_gun", methods=["POST"])
def create_machine_gun():
    damage_1 = request.json["damage_1"]
    damage_2 = request.json["damage_2"]
    damage_3 = request.json["damage_3"]

    m = add_machine_gun(damage_1, damage_2, damage_3)
    return jsonify(plane_schema.dump(m))
