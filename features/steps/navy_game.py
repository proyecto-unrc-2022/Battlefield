import json

from behave import *
from flask import url_for

from app import db
from app.daos.user_dao import add_user
from app.navy.services.navy_game_service import navy_game_service
from app.navy.models.navy_game import NavyGame
from app.models.user import User


@given('I am logged in as "user1"')
def step_impl(context):
    add_user("user1", "12345", "user1@user1.com")
    context.body = {"username": "user1", "password": "12345"}
    context.headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("auth.login"), json=context.body, headers=context.headers
    )
    context.user1 = User.query.filter_by(username="user1").first()
    context.token = json.loads(context.page.text)
    assert context.page

@when(u'I create a new game')
def step_impl(context):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {"user1_id": context.user1.id}
    context.page = context.client.post(
        url_for("navy.new_navy_game"), json=body, headers=headers
    )
    assert context.page

@then(u'The game should be created')
def step_impl(context):
    assert context.page.status_code == 201

@when(u'I try to create a game with an incorrect request body')
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

@then(u'I should get an error')
def step_impl(context):
    assert context.page.status_code == 400

@given(u'Some games have been created')
def step_impl(context):
    data = {"user1_id": context.user1.id}
    navy_game_service.add(data)
    navy_game_service.add(data)

@when(u'I try to get all navy games in the app')
def step_impl(context):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.get(
        url_for("navy.get_navy_games"), headers=headers
    )
    assert context.page


@then(u'I should get all navy games in the app')
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    assert context.page.status_code == 200
    assert len(data) != 0

@when(u'I try to get all navy games for user1')
def step_impl(context):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.get(
        url_for("navy.get_navy_games", user_id=context.user1.id), headers=headers
    )
    assert context.page


@then(u'I should get all navy games for user1')
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    print(data)
    assert context.page.status_code == 200
    assert len(data) != 0

@when(u'I try to get the game with id 1')
def step_impl(context):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.get(
        url_for("navy.get_navy_game", id=1), headers=headers
    )
    assert context.page


@then(u'I should get the game with id 1')
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    assert context.page.status_code == 200
    assert data["id"] == 1

@given(u'A game by another user has been created')
def step_impl(context):
    add_user("user2", "123", "user2@correo.com")
    user2 = context.user1 = User.query.filter_by(username="user2").first()
    data = {"user1_id": user2.id}
    context.game_created = navy_game_service.add(data)

@when(u'I try to join to the game')
def step_impl(context):
    body = {"user2_id": context.user1.id}
    headers = {
      "Content-Type": "application/json",
      "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.patch(
        url_for("navy.update_navy_game", id=context.game_created.id), json=body, headers=headers
    )
    assert context.page

@then(u'The game should be updated')
def step_impl(context):
    data = json.loads(context.page.text)["data"]
    assert context.page.status_code == 200
    assert data["user2_id"] == context.user1.id

@when(u'I try to join to the game with an incorrect user')
def step_impl(context):
    body = {"user2_id": 500}
    headers = {
      "Content-Type": "application/json",
      "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.patch(
        url_for("navy.update_navy_game", id=context.game_created.id), json=body, headers=headers
    )
    assert context.page

@when(u'I try to delete the game with id 1')
def step_impl(context):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f'Bearer {context.token["token"]}',
    }
    context.page = context.client.delete(
        url_for("navy.delete_navy_game", id=1), headers=headers
    )
    assert context.page


@then(u'The game with id 1 should be deleted')
def step_impl(context):
    assert context.page.status_code == 200