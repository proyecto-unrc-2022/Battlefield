import json

from behave import *
from flask import url_for
from steps.navy.test_utils import test_utils

EXPECTED_ERRORS = {
    "Game not found": "navy_game_id",
    "Invalid move": "_schema",
    "User not found": "user_id",
    "Must be one of: N, S, E, W, SE, SW, NE, NW.": "course",
    "Can't move more than 3 spaces": "_schema",
    "The movement is a negative distance": "_schema",
    "Invalid ship in game": "_schema",
    "Ship not found":"_schema"
}


@given("Is my turn")
def step_impl(context):

    from app.navy.services.navy_game_service import navy_game_service

    context.game = navy_game_service.add({"user1_id": context.user1.id})

    assert context.game


@given(
    "The user '{id_user:d}' has a '{ship_name}' in '{pos_x:d}','{pos_y:d}' with course '{course}'"
)
def step_impl(context, ship_name, pos_x, pos_y, course, id_user):

    from app.navy.services.ship_service import ship_service

    context.ship = ship_service.add(
        test_utils.json_ship(ship_name, pos_x, pos_y, course, id_user, context.game.id)
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
            context.user1.id,
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


@when("I try to move in a game with an invalid action like shoot and move")
def step_impl(context):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user1.id,
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


@then("I should see an error message '{error_msj}'")
def step_impl(context, error_msj):
    print(context.page.text)

    message = json.loads(context.page.text)
    value = EXPECTED_ERRORS[error_msj]
    assert message[value][0] == error_msj


@when("I try to move in a game with a user that doesn't exist")
def step_impl(context):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            -1,
            context.ship.course,
            0,
            context.game.id,
            context.ship.missile_type_id,
            context.ship.id,
            2,
        ),
        headers=context.headers,
    )

    assert context.page


@when("I try to move in a game with an incorrect direction like '{course}'")
def step_impl(context, course):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user1.id,
            course,
            0,
            context.game.id,
            context.ship.missile_type_id,
            context.ship.id,
            2,
        ),
        headers=context.headers,
    )

    assert context.page


@when("I try to move in a game with an incorrect distance like '{move}'")
def step_impl(context, move):

    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user1.id,
            context.ship.course,
            0,
            context.game.id,
            context.ship.missile_type_id,
            context.ship.id,
            move,
        ),
        headers=context.headers,
    )

    assert context.page


@when("I try to move in a game with an incorrect move range like '{move}'")
def step_impl(context, move):
    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user1.id,
            context.ship.course,
            0,
            context.game.id,
            context.ship.missile_type_id,
            context.ship.id,
            move,
        ),
        headers=context.headers,
    )

    assert context.page


@when("I try to move user 2's ship")
def step_impl(context):
    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user1.id,
            context.ship.course,
            0,
            context.game.id,
            context.ship.missile_type_id,
            context.ship.id,
            1,
        ),
        headers=context.headers,
    )

    assert context.page


@when("I try to move a ship that doesn't exist in the game")
def step_impl(context):
    context.headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }

    context.page = context.client.post(
        url_for("navy.action"),
        json=test_utils.json_action(
            context.user1.id,
            context.ship.course,
            0,
            context.game.id,
            context.ship.missile_type_id,
            3,
            2,
        ),
        headers=context.headers,
    )

    assert context.page
