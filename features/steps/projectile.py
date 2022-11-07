import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane, add_projectile, get_plane
from app.models.airforce.air_force_battlefield import Battlefield
from app.models.airforce.air_force_game import AirForceGame
from app.models.airforce.plane import PlaneSchema, ProjectileSchema
from app.models.user import User

plane_schema = PlaneSchema()
proj_schema = ProjectileSchema()
air_force_game = AirForceGame()


@given("a users logged")
def step_impl(context):
    user_a = User(username="Carlitos", email="carlitos@gmail.com", password="1234")
    db.session.add(user_a)
    user_b = User(username="username", email="username@gmail.com", password="1234")
    db.session.add(user_b)
    db.session.commit()

    context.player_a = user_a.id
    context.player_b = user_b.id


@when("user_a create the game")
def step_impl(context):
    context.response = context.client.post(
        url_for("air_force.new_game", player=context.player_a)
    )
    print(context.response)
    context.game_id = context.response.json.get("game_id")
    assert context.response.status_code == 200


@when("user_b join in game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player_b, id=context.game_id)
    )
    assert context.response.status_code == 200


@when("player_a add his plane")
def step_impl(context):
    players = context.client.get(url_for("air_force.get_players", id=0))
    players = players.json
    context.player_a = players.get("player_a")
    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=3,
        coor_x=5,
        coor_y=5,
    )
    context.x = 5
    context.course = 3
    context.y = 5
    projectile = add_projectile(speed=5, damage=10)
    context.plane.projectile.append(projectile)

    body = {
        "id": context.game_id,
        "player": context.player_a,
        "plane": context.plane.id,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    headers = {"Content-Type": "application/json"}
    context.page = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    assert context.page


@when("player_b add his plane")
def step_impl(context):
    players = context.client.get(url_for("air_force.get_players", id=0))
    players = players.json
    context.player_b = players.get("player_b")

    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=2,
        coor_x=15,
        coor_y=5,
    )
    context.x = 15
    context.course = 2
    context.y = 5
    projectile = add_projectile(speed=5, damage=10)
    context.plane.projectile.append(projectile)

    body = {
        "id": context.game_id,
        "player": context.player_b,
        "plane": context.plane.id,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    headers = {"Content-Type": "application/json"}

    context.page = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    assert context.page


@then("a '200' responses")
def step_impl(context):
    raw_response = context.client.get(
        url_for("air_force.get_battlefield_status", id=context.game_id)
    ).json
    raw_expected = [
        {"course": 3, "flying_obj": 1, "player": 1, "x": 5, "y": 5},
        {"course": 2, "flying_obj": 2, "player": 2, "x": 15, "y": 5},
        {"course": 3, "flying_obj": 1, "player": "1", "x": 5, "y": 6},
        {"course": 2, "flying_obj": 2, "player": "2", "x": 16, "y": 5},
    ]
    assert raw_expected == raw_response


@when("player_a create a projectile")
def step_impl(context):
    context.response = context.client.post(
        url_for(
            "air_force.create_projectile", id=context.game_id, player=context.player_a
        )
    )


@when("player_b create a projectile")
def step_impl(context):
    context.response = context.client.post(
        url_for(
            "air_force.create_projectile", id=context.game_id, player=context.player_b
        )
    )
