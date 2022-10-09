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
    context.page = context.client.get(url_for("undergame.new_game", host_id=player.id))

    assert context.page


@then("a new game with host '{username}' is registered")
def step_impl(context, username):
    data = json.dumps(context.page.text)
    player = context.players[username]

    assert data["host_id"] == player.id


@then("a game with an empty board is returned")
def step_impl(context):
    # board = context.game.board
    # for i in range(board.height):
    #     for j in range(board.width):
    #         assert(board.is_empty((i,j)))

    data = json.dumps(context.page.text)
    assert data["submerged_objects"] == []


# PLAYER OF A GAME TRIES TO CREATE ANOTHER


@given("the user '{username}' is in a game")
def step_impl(context, username):
    player = context.players[username]
    context.game = game_dao.create(player.id)


@then("the system informs failure")
def step_impl(context):
    assert context.page.status_code == 409
