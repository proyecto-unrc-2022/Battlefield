import json

from behave import *
from flask import url_for

from app.daos.user_dao import add_user
from app.models.user import User
from app.navy.services.navy_game_service import navy_game_service
from steps.navy.test_utils import test_utils



@given("a user '{id}' logged in")
def step_impl(context, id):
    username, email = test_utils.generate_username_and_email(id)
    add_user(username, "12345", email)
    context.body = {"username": username, "password": "12345"}
    context.headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("auth.login"), json=context.body, headers=context.headers
    )
    context.user1 = User.query.filter_by(username=username).first()
    context.token = json.loads(context.page.text)
    assert context.page


@when("I create a new game")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.post(
        url_for("navy.new_navy_game"), headers=headers
    )
    assert context.page


@then("The game should be created")
def step_impl(context):
    assert context.page.status_code == 201


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


@then("an error should appear")
def step_impl(context):
    assert context.page.status_code == 400


@given("Some games have been created")
def step_impl(context):
    data = {"user1_id": context.user1.id}
    navy_game_service.add(data)
    navy_game_service.add(data)


@when("I try to get all navy games in the app")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.get(url_for("navy.get_navy_games"), headers=headers)
    assert context.page


@then("I should get all navy games in the app")
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    assert context.page.status_code == 200
    assert len(data) != 0


@when("I try to get all navy games for user1")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.get(
        url_for("navy.get_navy_games", user_id=context.user1.id), headers=headers
    )
    assert context.page


@then("I should get all navy games for user1")
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    print(data)
    assert context.page.status_code == 200
    assert len(data) != 0


@when("I try to get the game with id 1")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.get(
        url_for("navy.get_navy_game", id=1), headers=headers
    )
    assert context.page


@then("I should get the game with id 1")
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    assert context.page.status_code == 200
    assert data["id"] == 1


@given("A game by another user has been created")
def step_impl(context):
    add_user("user2", "123", "user2@correo.com")
    user2 = User.query.filter_by(username="user2").first()
    data = {"user1_id": user2.id}
    context.game_created = navy_game_service.add(data)


@when("I try to join to the game")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.patch(
        url_for("navy.update_navy_game", id=context.game_created.id),
        headers=headers,
    )
    assert context.page


@then("The game should be updated")
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    assert context.page.status_code == 200
    assert data["user_2"]["id"] == context.user1.id


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


@when("I try to delete the game with id 1")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.delete(
        url_for("navy.delete_navy_game", id=1), headers=headers
    )
    assert context.page


@then("The game with id 1 should be deleted")
def step_impl(context):
    assert context.page.status_code == 200
