import json

from behave import *
from flask import url_for
from steps.navy.test_utils import test_utils


@given(
    "the user '{user_id:d}' created a '{ship_name}' in '{pos_x:d}', '{pos_y:d}' with course '{course}' and '{hp:d}' hp in the NavyGame '{game_id:d}'"
)
def step_impl(context, user_id, ship_name, pos_x, pos_y, course, hp, game_id):
    from app.navy.services.ship_service import ship_service

    try:
        context.ships.update(
            {
                user_id: test_utils.add_test_ship(
                    name=ship_name,
                    pos_x=pos_x,
                    pos_y=pos_y,
                    course=course,
                    hp=hp,
                    navy_game_id=game_id,
                    user_id=user_id,
                )
            }
        )
    except:
        context.ships = {}
        context.ships[user_id] = test_utils.add_test_ship(
            name=ship_name,
            pos_x=pos_x,
            pos_y=pos_y,
            course=course,
            hp=hp,
            navy_game_id=game_id,
            user_id=user_id,
        )

    ships_db = ship_service.get_by(navy_game_id=game_id)

    assert context.ships[user_id] in ships_db


@when(
    "the user '{user_id:d}' creates a '{ship_name}' in '{pos_x:d}', '{pos_y:d}' with course '{course}' for the NavyGame '{game_id:d}'"
)
def step_impl(context, user_id, ship_name, pos_x, pos_y, course, game_id):
    headers = test_utils.get_header(context.tokens[user_id])
    body = test_utils.json_ship(ship_name, pos_x, pos_y, course, user_id, game_id)
    context.pages[user_id] = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    assert context.pages[user_id]


@then("the ship of user '{user_id:d}' should be created successfully")
def step_impl(context, user_id):
    assert context.pages[user_id].status_code == 201


@then("the ship of user '{user_id:d}' shouldn't be created")
def step_impl(context, user_id):
    assert context.pages[user_id].status_code == 400


@then(
    "the user '{user_id:d}' should see his ship with the course '{course}' at '{pos_x:d}', '{pos_y:d}' with '{hp:d}' hp in the NavyGame '{game_id:d}'"
)
def step_impl(context, user_id, course, pos_x, pos_y, hp, game_id):
    current_game = json.loads(context.pages[user_id].text)["data"]

    assert context.pages[user_id].status_code == 200
    assert current_game["id"] == game_id
    assert current_game["ship"]["course"] == course
    assert (
        current_game["ship"]["pos_x"] == pos_x
        and current_game["ship"]["pos_y"] == pos_y
    )
    assert current_game["ship"]["hp"] == hp
