import ast
import json

from flask import url_for

from app import db
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
