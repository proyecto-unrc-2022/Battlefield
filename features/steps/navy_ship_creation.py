import json

from behave import *
from flask import url_for

from app.models.user import User
from app.navy.services.navy_game_service import navy_game_service
from steps.navy.test_utils import test_utils

@given("the user '{id:d}' creates a NavyGame")
def step_impl(context, id):
    print(context.bodies)
    print(context.pages)
    print(context.users)
    print(context.tokens)
    data = {"user1_id": context.user1.id}
    context.game_created = navy_game_service.add(data)

@given('the user "{id}" joins the NavyGame')
def step_impl(context, id):
    data = {"user2_id": context.user2.id}
    game_id = context.game_created.id
    context.game_created = navy_game_service.join(data, game_id)


@when('the user "{id}" creates a "{name}" in "{x:d}", "{y:d}" with course "{course}"')
def step_impl(context, id, name, x, y, course):
    """ headers = {
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
 """

@then("the ship should be created successfully")
def step_impl(context):
    assert context.page.status_code == 201
