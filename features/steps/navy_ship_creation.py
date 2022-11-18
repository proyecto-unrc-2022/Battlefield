import json

from behave import *
from flask import url_for

@given("the user '{user_id:d}' created a '{ship_name}' in '{pos_x:d}', '{pos_y:d}' with course '{course}' for the NavyGame '{game_id:d}'")
def step_impl(context, user_id, ship_name, pos_x, pos_y, course, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    current_game = json.loads(context.games_created[game_id].text)["data"]
    print(current_game)
    body = {
        "name": ship_name,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "course": course,
        "user_id": context.users[user_id].id,
        "navy_game_id": current_game["id"],
    }
    context.pages[user_id] = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    assert context.pages[user_id]

@when("the user '{user_id:d}' creates a '{ship_name}' in '{pos_x:d}', '{pos_y:d}' with course '{course}' for the NavyGame '{game_id:d}'")
def step_impl(context, user_id, ship_name, pos_x, pos_y, course, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    current_game = json.loads(context.games_created[game_id].text)["data"]
    print(current_game)
    body = {
        "name": ship_name,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "course": course,
        "user_id": context.users[user_id].id,
        "navy_game_id": current_game["id"],
    }
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