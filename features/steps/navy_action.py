import json

from behave import *
from flask import url_for
from steps.navy.test_utils import test_utils


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
        url_for("navy.new_action"), json=body, headers=headers
    )


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
        url_for("navy.new_action"), json=body, headers=headers
    )


@when(
    "the user '{user_id:d}' turns his ship to '{course}', moves it '{distance:d}' cells and attacks for round '{round:d}' in NavyGame '{game_id:d}'"
)
def step_impl(context, user_id, course, distance, round, game_id):
    headers = test_utils.get_header(context.tokens[user_id])
    current_ship = context.ships[user_id]
    body = test_utils.json_action(
        user_id,
        course,
        1,
        game_id,
        current_ship.missile_type_id,
        current_ship.id,
        distance,
        round,
    )
    context.pages[user_id] = context.client.post(
        url_for("navy.new_action"), json=body, headers=headers
    )


@when(
    "the user '{user1_id:d}' turns users '{user2_id:d}' ship to '{course}' and moves it '{distance:d}' cells for round '{round:d}' in NavyGame '{game_id:d}'"
)
def step_impl(context, user1_id, user2_id, course, distance, round, game_id):
    headers = test_utils.get_header(context.tokens[user1_id])
    current_ship = context.ships[user2_id]
    body = test_utils.json_action(
        user1_id,
        course,
        0,
        game_id,
        current_ship.missile_type_id,
        current_ship.id,
        distance,
        round,
    )
    context.pages[user1_id] = context.client.post(
        url_for("navy.new_action"), json=body, headers=headers
    )


@then("the user '{user_id:d}' should see an error message '{error_msg}'")
def step_impl(context, user_id, error_msg):
    message = json.loads(context.pages[user_id].text)["message"]
    value = test_utils.EXPECTED_ERRORS[error_msg]
    assert message[value][0] == error_msg
