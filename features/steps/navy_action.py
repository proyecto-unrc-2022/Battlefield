import json

from behave import *
from flask import url_for
from steps.navy.test_utils import test_utils

from app.daos.user_dao import add_user
from app.models.user import User

EXPECTED_ERRORS = {
    "game": "Game not found",
}


@given('I am logged "user"')
def step_impl(context):
    add_user("user1", "12345", "user1@user1.com")
    context.body = {"username": "user1", "password": "12345"}
    context.headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("auth.login"), json=context.body, headers=context.headers
    )
    context.user = User.query.filter_by(username="user1").first()
    assert context.user.email == "user1@user1.com"
    assert context.page


@given("the app initialized")
def step_impl(context):
    context.token = json.loads(context.page.text)
    assert context.token


@given("Is my turn")
def step_impl(context):

    from app.navy.services.navy_game_service import navy_game_service

    context.game = navy_game_service.add({"user1_id": context.user.id})

    assert context.game


@given("I have a '{ship_name}' in '{pos_x:d}','{pos_y:d}' with course '{course}'")
def step_impl(context, ship_name, pos_x, pos_y, course):

    from app.navy.services.ship_service import ship_service

    context.ship = ship_service.add(
        test_utils.json_ship(
            ship_name, pos_x, pos_y, course, context.user.id, context.game.id
        )
    )


@when("I try to move in a game that doesn't exist")
def step_impl(context):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user.id,
            context.ship.course,
            1,
            4,
            context.ship.missile_type_id,
            context.ship.id,
            3,
        ),
        headers=context.headers,
    )

    assert context.page


@then("I should see an error message '{error_msj}' about the game")
def step_impl(context, error_msj):

    print(context.page.text)
    message = json.loads(context.page.text)

    assert message["navy_game_id"][0] == error_msj
    # assert message["_schema"][0] == error_msj


# -------------------------------------------------------------------------------


@when("I try to move in a game with an invalid action like shoot and move")
def step_impl(context):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user.id,
            context.ship.course,
            1,
            context.game.id,
            context.ship.missile_type_id,
            context.ship.id,
            2,
        ),
        headers=context.headers,
    )

    assert context.page


@then("I should see an error message '{error}'")
def step_impl(context, error):
    print(context.page.text)
    message = json.loads(context.page.text)
    assert message["_schema"][0] == error
