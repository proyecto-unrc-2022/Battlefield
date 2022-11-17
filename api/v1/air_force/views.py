import json

from flask import Blueprint, Response, jsonify, request
from flask_cors import CORS

from api import token_auth, verify_token
from app.daos.airforce.plane_dao import add_machine_gun, add_plane, add_projectile
from app.models.airforce.air_force_game import (
    AirForceGame,
    CheckCourse,
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
air_force_game = []


@air_force.route("/new_game", methods=["POST"])
@token_auth.login_required
def new_game():
    token = request.headers["authorization"].split()[1]
    player = verify_token(token).id
    game = AirForceGame()
    air_force_game.append(game)
    game_id = len(air_force_game) - 1
    command = JoinGame(player=player, air_force_game=game)
    try:
        game.execute(command)
    except:
        return Response(status=400)
    return jsonify({"game_id": game_id})


@air_force.route("/join/game/<id>", methods=["PUT"])
@token_auth.login_required
def join_in_game(id):
    token = request.headers["authorization"].split()[1]
    player = verify_token(token).id
    game = air_force_game[int(id)]
    command = JoinGame(player=player, air_force_game=game)
    try:
        game.execute(command)
    except:
        return Response(status=400)
    command = GetPlayers(game)
    print(player)
    return jsonify(game.execute(command))


@air_force.route("/get_players/game_id/<id>", methods=["GET"])
def get_players(id):
    game = air_force_game[int(id)]
    command = GetPlayers(game)
    return jsonify(game.execute(command))


@air_force.route("/choose_plane", methods=["PUT"])
@token_auth.login_required
def choose_plane_and_position():
    token = request.headers["authorization"].split()[1]
    player = verify_token(token).id
    game = air_force_game[int(request.json["id"])]
    plane = request.json["plane"]
    x = request.json["x"]
    y = request.json["y"]
    course = request.json["course"]

    plane = Plane.query.filter_by(id=plane).first()
    try:
        command = ChoosePlane(
            course=course, plane=plane, x=x, y=y, player=player, air_force_game=game
        )
        dic = game.execute(command)
        print("dicc", dic)
        print("airforce game:", air_force_game)
        return jsonify(dic.to_dict())  # Response(status=201)
    except:
        return Response(status=400)


@air_force.route("game_id/<id>//course/<course>/", methods=["PUT"])
@token_auth.login_required
def fligth(id, course):
    token = request.headers["authorization"].split()[1]
    player = verify_token(token).id
    game = air_force_game[int(id)]
    try:
        game.execute(CheckCourse(course, player, game))
        command = MovePlane(course, player, game)
        game.add_command(command, player)
        print("player_a", game.player_a, "player_b", game.player_b)
        print("comandos en volar: ", game.new_commands)
        return Response(status=201)
    except:
        return Response(status=400)


@air_force.route("/game/<id>/new_projectile", methods=["POST"])
@token_auth.login_required
def create_projectile(id):
    token = request.headers["authorization"].split()[1]
    player = verify_token(token).id
    game = air_force_game[int(id)]
    command = LaunchProjectile(player, game)
    print("comandos en disparar: ", game.new_commands)
    try:
        game.add_command(command, player)
        return Response(status=200)  # jsonify(dic.to_dict())
    except:
        return Response(status=400)


@air_force.route("get_battlefield_status/game_id/<id>", methods=["GET"])
def get_battlefield_status(id):
    game = air_force_game[int(id)]
    command = GetBattlefieldStatus(game.battlefield, game)
    obj_list = game.execute(command)
    return jsonify(obj_list)


# @air_force.route("/game/plane/<plane_id>", methods=["GET"])
# def get_plane(plane_id):
# plane = get_plane_dao(plane_id)
# return jsonify(plane_schema.dump(plane))


@air_force.route("/players/<player>/plane", methods=["GET"])
def get_player_plane(player):
    plane = air_force_game.get_player_plane(player)
    return jsonify(plane)


# @air_force.route("/newplane", methods=["POST"])
# def put_plane():
#     name = request.json["name"]
#     size = request.json["size"]
#     speed = request.json["speed"]
#     health = request.json["health"]
#     course = request.json["course"]
#     coor_x = request.json["coor_x"]
#     coor_y = request.json["coor_y"]
#     p = add_plane(name, size, speed, health, course, coor_x, coor_y)
#     return jsonify(plane_schema.dump(p))


@air_force.route("/initdb", methods=["POST"])
def init_db():
    f = open("./api/v1/air_force/planes.json")
    data = json.load(f)
    for plane in data["planes"]:
        name = plane["name"]
        size = plane["size"]
        speed = plane["speed"]
        health = plane["health"]
        cant_projectile = plane["cant_projectile"]
        p = add_plane(name, size, speed, health, cant_projectile)
    for projectile in data["projectile"]:
        speed = projectile["speed"]
        damage = projectile["damage"]
        plane = Plane.query.filter_by(name=projectile["plane"]).first().id
        add_projectile(speed=speed, damage=damage, plane_id=plane)
    return Response(status=200)


@air_force.route("/machine_gun", methods=["POST"])
def create_machine_gun():
    damage_1 = request.json["damage_1"]
    damage_2 = request.json["damage_2"]
    damage_3 = request.json["damage_3"]

    m = add_machine_gun(damage_1, damage_2, damage_3)
    return jsonify(plane_schema.dump(m))


@air_force.route("/attack", methods=["POST"])
def attack():
    return "boooom"
