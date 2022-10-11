import json

from behave import *
from flask import url_for

from app.daos.user_dao import add_user
from app.models.user import User

EXPECTED_ERRORS = {
    "game": "Game not found",
}


@given('I am logged in as "user"')
def step_impl(context):
    add_user("user1", "12345", "user1@user1.com")
    context.body = {"username": "user1", "password": "12345"}
    context.headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("auth.login"), json=context.body, headers=context.headers
    )
    context.user_1 = User.query.filter_by(username="user1").first()
    assert context.user_1.email == "user1@user1.com"
    assert context.page


@given("the app initialized")
def step_impl(context):
    context.token = json.loads(context.page.text)
    assert context.token


@given("Is my turn")
def step_impl(context):
    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.body = {"id_user_1": context.user_1.id}
    context.page = context.client.post(
        url_for("navy.create_game"), json=context.body, headers=context.headers
    )
    assert context.page


@when("I try to move in a game that doesn't exist")
def step_impl(context):
    data = {
        "id_user": context.user_1.id,
        "dir": "N",
        "attack": 0,
        "id_game": -1,
        "id_missile": 1,
        "id_ship": 1,
        "move": 3,
        "ship_type": 1,
    }

    context.page = context.client.post(
        url_for("navy.action"), json=data, headers=context.headers
    )
    assert context.page


@then("I should see an error message '{error_msj}' about the '{game}'")
def step_impl(context, error_msj, game):
    assert context.page.status_code == 400
