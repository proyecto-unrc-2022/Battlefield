import ast
import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane
from app.models.airforce.air_force_game import AirForceGame
from app.models.user import User


@given("logged user")
def step_impl(context):
    user = User(username="Jhon", email="jhon@email", password="pass")
    db.session.add(user)
    db.session.commit()
    context.player = user.id


@when("enter in empty game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player)
    )
    assert context.response.status_code is 200


@then("players id who are in the game are returned")
def step_impl(context):
    raw_expected = {"player_a": str(context.player), "player_b": None}
    raw_response = context.response.json

    response, expected = json.dumps(raw_expected, sort_keys=True), json.dumps(
        raw_response, sort_keys=True
    )
    print(response)
    print(expected)
    assert response == expected


@given("a second user")
def step_impl(context):
    user = User(username="Peter", email="Peter@email", password="pass")
    db.session.add(user)
    db.session.commit()
    context.player_b = user.id


@when("new user enter in the game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player_b)
    )
    assert context.response.status_code is 200


@then("two users info are returned")
def step_impl(context):
    raw_expected = {
        "player_a": str(1),  # esta croto esto ver mejor ;)
        "player_b": str(context.player_b),
    }
    raw_response = context.response.json
    response, expected = json.dumps(raw_expected, sort_keys=True), json.dumps(
        raw_response, sort_keys=True
    )
    assert response == expected


@given("a third user")
def step_impl(context):
    user = User(username="Vladimir", email="vodka@email", password="pass")
    db.session.add(user)
    db.session.commit()
    context.player_b = user.id


@when("new user try enter in the game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player_b)
    )


@then("exception are returned")
def step_impl(context):
    print(context.response.status_code)
    assert context.response.status_code == 400


@given("a user in the game and plane in db")
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


@when("choose a plane and his position")
def step_impl(context):
    context.response = context.client.put(
        url_for(
            "air_force.choise_plane_and_position",
            player=context.player,
            plane=context.plane.id,
            x=3,
            y=3,
            course=2,
        )
    )


@then("201 response are returned")
def step_impl(context):
    assert context.response.status_code == 201
