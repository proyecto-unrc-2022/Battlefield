import json

from flask import Blueprint, Response, jsonify, request
from flask_cors import CORS

from api import token_auth, verify_token
from app.daos.airforce.plane_dao import (
    add_machine_gun,
    add_plane,
    add_projectile,
    get_all_planes,
)
from app.models.airforce.air_force_game import AirForceGame
from app.models.airforce.commands.check_course import CheckCourse
from app.models.airforce.commands.choose_plane import ChoosePlane
from app.models.airforce.commands.game_ready import GameReady
from app.models.airforce.commands.get_battlefield_status import GetBattlefieldStatus
from app.models.airforce.commands.get_players import GetPlayers
from app.models.airforce.commands.join_game import JoinGame
from app.models.airforce.commands.launch_projectile import LaunchProjectile
from app.models.airforce.commands.move_plane import MovePlane
from app.models.airforce.commands.players_have_plane import PlayersHavePlane
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
    x = int(request.json["x"])
    y = int(request.json["y"])
    course = int(request.json["course"])

    plane = Plane.query.filter_by(id=plane).first()
    try:
        print(plane)
        command = ChoosePlane(
            course=course, plane=plane, x=x, y=y, player=player, air_force_game=game
        )
        game.execute(command)
        return jsonify(game.battlefield.get_status())  # Response(status=201)
    except Exception as e:
        print(e)
        return Response(str(e), status=400)


@air_force.route("game_id/<id>//course/<course>/", methods=["PUT"])
@token_auth.login_required
def fligth(id, course):
    token = request.headers["authorization"].split()[1]
    player = verify_token(token).id
    game = air_force_game[int(id)]
    try:
        from app.models.airforce.utils import get_player_plane as get

        print("new ", get(game.battlefield, player)[0].course)
        game.execute(CheckCourse(course, player, game))
        command = MovePlane(course, player, game)
        print("andaaaaa")
        game.add_command(command, player)
        return Response(status=201)
    except Exception as e:
        return Response(str(e), status=400)


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
    except Exception as e:
        print(e)
        return Response(str(e), status=400)


@air_force.route("/game/<id>/ready", methods=["GET"])
def game_ready(id):
    game = air_force_game[int(id)]
    command = GameReady(game)
    return jsonify(game.execute(command))


@air_force.route("/game/<id>/players/have/plane", methods=["GET"])
def game_players_have_plane(id):
    game = air_force_game[int(id)]
    command = PlayersHavePlane(game)
    return jsonify(game.execute(command))


@air_force.route("get_battlefield_status/game_id/<id>", methods=["GET"])
def get_battlefield_status(id):
    game = air_force_game[int(id)]
    command = GetBattlefieldStatus(game.battlefield, game)
    obj_list = game.execute(command)
    return jsonify(obj_list)


@air_force.route("/get/planes", methods=["GET"])
def get_plane():
    plane = get_all_planes()
    listPlane = {}
    for p in plane:
        listPlane[p.id] = plane_schema.dump(p)
    return listPlane


@air_force.route("/players/<player>/plane", methods=["GET"])
def get_player_plane(player):
    plane = air_force_game.get_player_plane(player)
    return jsonify(plane)


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
