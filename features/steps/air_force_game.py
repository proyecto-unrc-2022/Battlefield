import ast
import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane
from app.models.airforce.air_force_game import AirForceGame
from app.models.user import User

url_for_plane_position = "air_force.choice_plane_and_position"


@given("three logged user")
def step_impl(context):
    user_a = User(username="Jhon", email="jhon@email", password="pass")
    db.session.add(user_a)
    user_b = User(username="Peter", email="Peter@email", password="pass")
    db.session.add(user_b)
    user_c = User(username="Vladimir", email="vodka@email", password="pass")
    db.session.add(user_c)
    db.session.commit()

    context.player_a = user_a.id
    context.player_b = user_b.id
    context.player_c = user_c.id


@when("enter in empty game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player_a)
    )
    assert context.response.status_code is 200


@then("players id who are in the game are returned")
def step_impl(context):
    raw_expected = {"player_a": str(context.player_a), "player_b": None}
    raw_response = context.response.json

    response, expected = json.dumps(raw_expected, sort_keys=True), json.dumps(
        raw_response, sort_keys=True
    )
    assert response == expected


@when("second user enter in the game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player_b)
    )
    assert context.response.status_code is 200


@then("two users info are returned")
def step_impl(context):
    raw_expected = {
        "player_a": str(context.player_a),
        "player_b": str(context.player_b),
    }
    raw_response = context.response.json
    response, expected = json.dumps(raw_expected, sort_keys=True), json.dumps(
        raw_response, sort_keys=True
    )
    print(response)
    print(expected)

    assert response == expected


@when("new user try enter in the game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player_c)
    )


@then("status code 400 is returned")
def step_impl(context):
    print(context.response.status_code)
    assert context.response.status_code == 400


@given("player_a and plane in db")
def step_impl(context):
    context.player = AirForceGame.player_a
    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=3,
        coor_x=5,
        coor_y=5,
    )
    context.x = 3
    context.y = 3
    context.course = 2


@when("player_a choose a plane and his position")
def step_impl(context):
    body = {
        "player": context.player,
        "plane": context.plane.id,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    headers = {"Content-Type": "application/json"}
    context.response = context.client.put(
        url_for("air_force.choice_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    assert context.response


@when("player_b choose a plane and his position")
def step_impl(context):
    body = {
        "player": context.player,
        "plane": context.plane.id,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    headers = {"Content-Type": "application/json"}
    context.response = context.client.put(
        url_for("air_force.choice_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    assert context.response


@then("info of the new flying object are returned")
def step_impl(context):
    raw_response = context.response.json
    raw_expected = {
        "player": context.player,
        "flying_obj": context.plane.id,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    response, expected = json.dumps(raw_response, sort_keys=True), json.dumps(
        raw_expected, sort_keys=True
    )
    print(response)
    print(expected)
    assert response == expected


@when("choose a plane and position outside of map")
def step_impl(context):
    body = {
        "player": context.player,
        "plane": context.plane.id,
        "x": 21,
        "y": 11,
        "course": 2,
    }
    headers = {"Conten-Type": "application/json"}

    context.response = context.client.put(
        url_for(url_for_plane_position), data=json.dumps(body), headers=headers
    )
    assert context.response


@then("400 response are returned")
def step_impl(context):
    assert context.response.status_code == 400


@when("choose a plane and position in player_b position")
def step_impl(context):
    body = {
        "player": context.player,
        "plane": context.plane.id,
        "x": 12,
        "y": 5,
        "course": 2,
    }
    headers = {"Conten-Type": "application/json"}

    context.response = context.client.put(
        url_for(url_for_plane_position), data=json.dumps(body), headers=headers
    )
    assert context.response


@then("Error status code are returned")
def step_impl(context):
    assert context.response.status_code == 400


@given("player_b in the game and plane in db")
def step_impl(context):
    context.player = AirForceGame.player_b
    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=3,
        coor_x=5,
        coor_y=5,
    )
    context.x = 13
    context.y = 6
    context.course = 4


@when("choose a plane and position in player_a position")
def step_impl(context):
    body = {
        "player": context.player,
        "plane": context.plane.id,
        "x": 1,
        "y": 5,
        "course": 2,
    }
    headers = {"Conten-Type": "application/json"}

    context.response = context.client.put(
        url_for(url_for_plane_position), data=json.dumps(body), headers=headers
    )
    assert context.response


@given("a battlefield with player_a's plane")
def step_impl(context):
    context.player = AirForceGame.player_a


@when("player_a moves his plane")
def step_impl(context):
    context.response = context.client.put(
        url_for(
            "air_force.fligth",
            player=context.player,
            course=2,
        )
    )


@then("201 response code are returned")
def step_impl(context):
    assert context.response.status_code == 201
