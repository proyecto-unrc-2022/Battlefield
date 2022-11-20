import json

from behave import *
from flask import url_for

from app.daos.user_dao import add_user
from app.models.user import User
from steps.navy.test_utils import test_utils

@given("a user '{user_id:d}' logged in")
def step_impl(context, user_id):
    username, email = test_utils.generate_username_and_email(user_id)
    add_user(username, "12345", email)
    context.headers = {"Content-Type": "application/json"}
    try:    
        context.bodies[user_id] = {"username": username, "password": "12345"}
        context.pages[user_id] = context.client.post(
            url_for("auth.login"), json=context.bodies[user_id], headers=context.headers
        )
        context.users[user_id] = User.query.filter_by(username=username).first()
        context.tokens[user_id] = json.loads(context.pages[user_id].text)
    except:
        context.bodies = {}
        context.pages = {}
        context.users = {}
        context.tokens = {}
        
        context.bodies.update({user_id:{"username": username, "password": "12345"}})
        context.pages[user_id] = context.client.post(
            url_for("auth.login"), json=context.bodies[user_id], headers=context.headers
        )
        context.users[user_id]=User.query.filter_by(username=username).first()
        context.tokens[user_id] = json.loads(context.pages[user_id].text)
    
    assert context.pages[user_id]


@when("the user '{user_id:d}' creates a NavyGame '{game_id:d}'")            
def step_impl(context, user_id, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }

    context.pages[user_id] = context.client.post(
        url_for("navy.new_navy_game"), headers=headers
    )
    try:
        context.games_created[game_id] = context.pages[user_id]
    except:
        context.games_created = {}
        context.games_created[game_id] = context.pages[user_id]


@given("the user '{user_id:d}' created a NavyGame '{game_id:d}'")           
def step_impl(context, user_id, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    context.pages[user_id] = context.client.post(
        url_for("navy.new_navy_game"), headers=headers
    )
    try:
        context.games_created[game_id] = context.pages[user_id]
    except:
        context.games_created = {}
        context.games_created[game_id] = context.pages[user_id]
        
    assert context.pages[user_id]
    assert context.games_created
    assert context.pages[user_id].status_code == 201


@then("the user '{user_id:d}' should see that the NavyGame was created")
def step_impl(context, user_id):
    assert context.pages[user_id].status_code == 201


@when("the user '{user_id:d}' tries to get all NavyGames in the app")
def step_impl(context,user_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    context.pages[user_id] = context.client.get(url_for("navy.get_navy_games"), headers=headers)
    assert context.pages[user_id]


@then("the user '{user_id:d}' should get all NavyGames in the app")
def step_impl(context, user_id):
    data = json.loads(context.pages[user_id].text)["data"]
    assert context.pages[user_id].status_code == 200
    assert len(data) != 0


@when("the user '{user_id:d}' tries to get the NavyGame '{game_id:d}'")
def step_impl(context, user_id, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    context.pages[user_id] = context.client.get(
        url_for("navy.get_navy_game", id=game_id), headers=headers
    )
    assert context.pages[user_id]


@then("the user '{user_id:d}' should get the NavyGame '{game_id:d}'")
def step_impl(context, user_id, game_id):
    data = json.loads(context.pages[user_id].text)["data"]
    assert context.pages[user_id].status_code == 200
    assert data["id"] == game_id


@when("the user '{user_id:d}' tries to join the NavyGame '{game_id:d}'")
def step_impl(context, user_id, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    context.pages[user_id] = context.client.patch(
        url_for("navy.update_navy_game", id=game_id),
        headers=headers,
    )
    context.games_created[game_id] = context.pages[user_id]
    assert context.pages[user_id]


@given("the user '{user_id:d}' joined the NavyGame '{game_id:d}'")
def step_impl(context, user_id, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    context.pages[user_id] = context.client.patch(
        url_for("navy.update_navy_game", id=game_id),
        headers=headers,
    )
    context.games_created[game_id] = context.pages[user_id]
    assert context.pages[user_id].status_code == 200


@then("the user '{user_id:d}' should see that the NavyGame was updated")
def step_impl(context, user_id):
    data = json.loads(context.pages[user_id].text)["data"]
    assert context.pages[user_id].status_code == 200
    assert data["user_2"]["id"] == context.users[user_id].id


@when("the user '{user_id:d}' deletes the NavyGame '{game_id:d}'")
def step_impl(context, user_id, game_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.tokens[user_id]["token"]}',
    }
    context.pages[user_id] = context.client.delete(
        url_for("navy.delete_navy_game", id=game_id), headers=headers
    )
    assert context.pages[user_id]


@then("the user '{id:d}' should see that the NavyGame was deleted")
def step_impl(context, id):
    assert context.pages[id].status_code == 200


@when("I try to join to the game with an incorrect user")
def step_impl(context):
    body = {"user2_id": 500}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.patch(
        url_for("navy.update_navy_game", id=context.game_created.id),
        json=body,
        headers=headers,
    )
    assert context.page


@when("I try to create a game with an incorrect request body")                        
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {"user_id": 255}
    context.page = context.client.post(
        url_for("navy.new_navy_game"), json=body, headers=headers
    )
    assert context.page
