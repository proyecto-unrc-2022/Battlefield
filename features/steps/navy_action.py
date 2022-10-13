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
    """context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    """
    from app.navy.daos.navy_game_dao import navy_game_dao
    from app.navy.models.navy_game import NavyGame

    navy_game = NavyGame(10, 20, context.user_1.id)
    navy_game_dao.add_or_update(navy_game)
    context.game_id = navy_game.id

    assert True


@when("I try to move in a game that doesn't exist")
def step_impl(context):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    from app.navy.daos.ship_dao import ship_dao
    from app.navy.models.ship import Ship

    ship_dao.add_or_update(
        Ship("Destroyer", 60, 3, 3, 5, 1, 3, 3, "N", context.user_1.id, context.game_id)
    )

    data = {
        "user_id": context.user_1.id,
        "course": "N",
        "attack": 0,
        "navy_game_id": 1,
        "missile_type_id": 1,
        "ship_id": 1,
        "move": 3,
    }

    context.page = context.client.post(
        url_for("navy.action"), json=data, headers=context.headers
    )
    assert context.page


@then("I should see an error message '{error_msj}' about the game")
def step_impl(context, error_msj):

    message = json.loads(context.page.text)

    assert message["_schema"][0] == error_msj


# -------------------------------------------------------------------------------


@given("I have a '{ship_name}' and can move '{ship_speed}' spaces with its")
def step_impl(context, ship_name, ship_speed):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    from app.navy.daos.ship_dao import ship_dao
    from app.navy.models.ship import Ship

    ship_dao.add_or_update(
        Ship(ship_name, 60, 3, 3, 5, 1, 3, 3, "N", context.user_1.id, context.game_id)
    )


@when("I try to move in a game with an invalid action like shoot and move")
def step_impl(context):
    data = {
        "user_id": context.user_1.id,
        "course": "N",
        "attack": 1,
        "navy_game_id": 1,
        "missile_type_id": 1,
        "ship_id": 1,
        "move": 3,
    }

    context.page = context.client.post(
        url_for("navy.action"), json=data, headers=context.headers
    )
    assert context.page


@then("I should see an error message '{error}'")
def step_impl(context, error):
    print(context.page.text)
    assert False
