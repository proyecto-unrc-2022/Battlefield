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
    context.player_a = AirForceGame.player_a
    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=3,
        coor_x=5,
        coor_y=5,
    )


@when("choose a plane and his position")
def step_impl(context):
    body = {
        "player": context.player_a,
        "plane": context.plane.id,
        "x": 3,
        "y": 3,
        "course": 2,
    }
    headers = {"Content-Type": "application/json"}
    context.response = context.client.put(
        url_for("air_force.choice_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    assert context.response


@then("201 response are returned")
def step_impl(context):
    raw_response = context.response.json
    raw_expected = [
        "1",
        {
            "coor_x": 5,
            "coor_y": 5,
            "course": 3,
            "health": 10,
            "name": "Hawker Tempest",
            "size": 1,
            "speed": 5,
        },
        3,
        3,
        2,
    ]
    response, expected = json.dumps(raw_response), json.dumps(raw_expected)
    assert response == expected


@when("choose a plane and position outside of map")
def step_impl(context):
    body = {
        "player": context.player_a,
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


@when("choose a plane and position in player_b position")
def step_impl(context):
    body = {
        "player": context.player_a,
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
    context.player_b = AirForceGame.player_b
    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=3,
        coor_x=5,
        coor_y=5,
    )


@when("choose a plane and position in player_a position")
def step_impl(context):
    body = {
        "player": context.player_b,
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
