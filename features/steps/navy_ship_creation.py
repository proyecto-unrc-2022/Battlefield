import json

from behave import *
from flask import url_for

from app.daos.user_dao import add_user
from app.models.user import User
from app.navy.services.navy_game_service import navy_game_service
from steps.navy.test_utils import test_utils

@given("a user '{id}' exists")
def step_impl(context, id):
    username, email = test_utils.generate_username_and_email(id)
    add_user(username, "123", email)
    context.user2 = User.query.filter_by(username=username).first()


@given("I've created a Navy Game")
def step_impl(context):
    # context.user1 given in backround (step implemented in navy_game steps)
    data = {"user1_id": context.user1.id}
    context.game_created = navy_game_service.add(data)


@given("another user joins the game I've created")
def step_impl(context):
    data = {"user2_id": context.user2.id}
    id = context.game_created.id
    context.game_created = navy_game_service.join(data, id)


@when("I try to create a \"Destroyer\" ship in ('2', '3') position, and 'N' direction")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {
        "name": "Destroyer",
        "pos_x": 2,
        "pos_y": 3,
        "course": "N",
        "user_id": context.user1.id,
        "navy_game_id": context.game_created.id,
    }
    context.page = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    assert context.page


@then("the ship should be created successfully")
def step_impl(context):
    assert context.page.status_code == 201


@given("another user creates a Navy Game")
def step_impl(context):
    data = {"user1_id": context.user2.id}
    context.game_created = navy_game_service.add(data)


@given("I join the game created by another user")
def step_impl(context):
    data = {"user2_id": context.user1.id}
    id = context.game_created.id
    context.game_created = navy_game_service.join(data, id)


@when("I try to create a \"Destroyer\" ship in ('5', '17') coords, and 'N' direction")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {
        "name": "Destroyer",
        "pos_x": 5,
        "pos_y": 17,
        "course": "N",
        "user_id": context.user1.id,
        "navy_game_id": context.game_created.id,
    }
    context.page = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    print(str(context.game_created))
    assert context.page


@when("I try to create ship with wrong name or course")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {
        "name": "Dinosaur",
        "pos_x": 2,
        "pos_y": 3,
        "course": "OK",
        "user_id": context.user1.id,
        "navy_game_id": context.game_created.id,
    }
    context.page = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    assert context.page


@when("I try to create ship with ('11', '9') coords")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {
        "name": "Destroyer",
        "pos_x": 11,
        "pos_y": 9,
        "course": "N",
        "user_id": context.user1.id,
        "navy_game_id": context.game_created.id,
    }
    context.page = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    assert context.page


@when("I try to create ship with ('2', '16') coords")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {
        "name": "Destroyer",
        "pos_x": 2,
        "pos_y": 16,
        "course": "N",
        "user_id": context.user1.id,
        "navy_game_id": context.game_created.id,
    }
    context.page = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    assert context.page


@when("I try to create ship with ('2', '6') coords")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {context.token["token"]}',
    }
    body = {
        "name": "Destroyer",
        "pos_x": 2,
        "pos_y": 6,
        "course": "N",
        "user_id": context.user1.id,
        "navy_game_id": context.game_created.id,
    }
    context.page = context.client.post(
        url_for("navy.new_ship"), json=body, headers=headers
    )
    assert context.page
