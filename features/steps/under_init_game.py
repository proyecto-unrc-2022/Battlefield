import json

from behave import given, then, when
from flask import url_for

from app import db
from app.daos.user_dao import add_user
from app.models.user import User
from app.underwater.daos.under_game_dao import game_dao

# BACKGROUND


@given("there exist some users and they are logged in")
def step_impl(context):
    context.players = {}
    for row in context.table:
        add_user(row["username"], row["password"], row["email"])
        new_user = db.session.query(User).where(User.username == row["username"]).one()
        context.players.update({row["username"]: new_user})


# CREATE A NEW GAME


@when("the user '{username}' asks for a new game")
def step_impl(context, username):
    player = context.players[username]
    context.page = context.client.get(url_for("underwater.new_game", host_id=player.id))

    assert context.page


@then("a new game with host '{username}' is registered")
def step_impl(context, username):
    data = json.loads(context.page.text)
    player = context.players[username]

    assert data["host_id"] == player.id


@then("a game with an empty board is returned")
def step_impl(context):
    data = json.loads(context.page.text)
    assert data["submarines"] == []
    assert data["torpedos"] == []


# PLAYER OF A GAME TRIES TO CREATE ANOTHER


@given("the user '{username}' is in a game of id '{id:d}'")
def step_impl(context, username, id):
    player = context.players[username]
    context.game = game_dao.create(player.id)
    context.game.id = id


@when("the user '{username}' asks to join the game of id '{id:d}'")
def step_impl(context, username, id):
    player = context.players[username]
    context.page = context.client.get(
        url_for("underwater.join_game", game_id=id, visitor_id=player.id)
    )
    assert context.page


@then("the system informs failure with code '{code:d}'")
def step_impl(context, code):
    print(context.page.status_code)
    assert context.page.status_code == code


# JOIN A GAME


@then("the system informs success")
def step_impl(context):
    assert context.page.status_code == 200


@then("a game with '{username}' is returned")
def step_impl(context, username):
    data = json.loads(context.page.text)
    player = context.players[username]
    assert data["host_id"] == player.id or data["visitor_id"] == player.id
