import json

from behave import *
from flask import url_for
from steps.navy.test_utils import test_utils


@given("Is my turn")
def step_impl(context):

    from app.navy.services.navy_game_service import navy_game_service

    data = {"user1_id": context.user1.id}
    context.game = navy_game_service.add(data)
    test_utils.add_test_game(context.game.id)

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


@then("the user '{user_id:d}' should see an error message '{error_msg}'")
def step_impl(context, user_id, error_msg):
    message = json.loads(context.pages[user_id].text)
    value = test_utils.EXPECTED_ERRORS[error_msg]
    assert message[value][0] == error_msg


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


@given("The game is already finished")
def step_impl(context):

    from app.navy.services.navy_game_service import navy_game_service

    data = {"user1_id": context.user1.id}
    context.game = navy_game_service.add(data)

    test_utils.add_test_game(context.game.id, winner=True)

    assert context.game


@when("I try to make an action in the ended game")
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
            2,
        ),
        headers=context.headers,
    )

    assert context.page


@when("I move the ship 3 positions to '{course}'")
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


@when("I try to move the ship again")
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
            3,
        ),
        headers=context.headers,
    )

    assert context.page


@when(
    "the user '{user_id:d}' turns his ship to '{course}' and moves it '{distance:d}' cells for round '{round:d}' in NavyGame '{game_id:d}'"
)
def step_impl(context, user_id, course, round, distance, game_id):
    headers = test_utils.get_header(context.tokens[user_id])
    current_ship = context.ships[user_id]
    body = test_utils.json_action(
        user_id,
        course,
        0,
        game_id,
        current_ship.missile_type_id,
        current_ship.id,
        distance,
        round,
    )
    context.pages[user_id] = context.client.post(
        url_for("navy.action"), json=body, headers=headers
    )
    print("mov" + context.pages[user_id].text)
    assert context.pages[user_id].status_code == 201


@when(
    "the user '{user_id:d}' turns his ship to '{course}' and attacks for round '{round:d}' in NavyGame '{game_id:d}'"
)
def step_impl(context, user_id, course, round, game_id):
    headers = test_utils.get_header(context.tokens[user_id])
    current_ship = context.ships[user_id]
    body = test_utils.json_action(
        user_id,
        course,
        1,
        game_id,
        current_ship.missile_type_id,
        current_ship.id,
        0,
        round,
    )
    context.pages[user_id] = context.client.post(
        url_for("navy.action"), json=body, headers=headers
    )
    print("attack" + context.pages[user_id].text)

    assert context.pages[user_id].status_code == 201
