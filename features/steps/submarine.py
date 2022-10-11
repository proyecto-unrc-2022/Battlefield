import json

from behave import *
from flask import url_for

from app import db
from app.daos.underwater.uw_game_dao import (
    add_submarine,
    create_game,
    get_game,
    update_game,
)
from app.daos.user_dao import add_user
from app.models.underwater.under_models import Submarine, UnderGame, boards
from app.models.user import User

# BACKGROUND


@given("there exists two users and they are logged in")
def step_impl(context):
    # add_user("player1", "player1", "player1@example.com")
    # context.player1 = (
    #     db.session.query(User).where(User.username == "player1").one_or_none()
    # )
    # add_user("player2", "player2", "player2@example.com")
    # context.player2 = (
    #     db.session.query(User).where(User.username == "player2").one_or_none()
    # )

    for row in context.table:
        add_user(row["username"], row["password"], row["email"])

    context.player1 = (
        db.session.query(User).where(User.username == "player1").one_or_none()
    )

    context.player2 = (
        db.session.query(User).where(User.username == "player2").one_or_none()
    )
    assert context.player1
    assert context.player2


# CREATE A NEW GAME


@when("the user 'player1' asks for a new underwater game")
def step_impl(context):
    context.page = context.client.get(
        url_for("underwater.new_game", host_id=context.player1.id)
    )
    assert context.page


@then("A new game is registered")
def step_impl(context):
    data = json.loads(context.page.text)
    game = db.session.query(UnderGame).filter_by(id=data["id"]).first()
    context.game = game
    assert game


@then("an empty board with one player is returned")
def step_impl(context):
    board = boards[context.game.id]
    for row in board.matrix:
        for cell in row:
            assert cell is None
    assert context.game.host


# JOIN A GAME


@given("there is a game with no visitor")
def step_impl(context):
    context.game = create_game(host_id=context.player1.id)
    assert context.game


@when("the user 'player2' joins that game")
def step_impl(context):
    context.page = context.client.get(
        url_for(
            "underwater.join_game",
            game_id=context.game.id,
            visitor_id=context.player2.id,
        )
    )
    assert context.page.status_code is 200


@then("the game now has the new visitor")
def step_impl(context):
    game = get_game(context.game.id)
    assert game
    assert game.visitor_id == context.player2.id


# GET THE SUBMARINE OPTIONS


@when("I receive a request to show the submarine options")
def step_impl(context):
    context.page = context.client.get(url_for("underwater.get_options"))
    assert context.page


@then("the options are returned")
def step_impl(context):
    options = json.loads(context.page.text)
    assert "0" in options
    assert "1" in options
    assert "2" in options
    assert "3" in options


# CHOOSE A SUBMARINE


@given("the user 'player1' is in a game of dimension '{h:d}'x'{w:d}' with visitor")
def step_impl(context, h, w):
    game = create_game(context.player1.id, h, w)
    context.game = update_game(game_id=game.id, visitor_id=context.player2.id)
    assert context.game


@when("the user 'player1' chooses a submarine")
def step_impl(context):
    data = {
        "game_id": context.game.id,
        "player_id": context.player1.id,
        "submarine_id": 1,
    }
    context.page = context.client.post(
        url_for("underwater.choose_submarine"), data=data
    )


@then("the game bounds the user to the choosen submarine successfully")
def step_impl(context):
    game = get_game(context.game.id)
    assert game.submarines[0].player_id == context.player1.id
    assert context.page.status_code is 200


# CHOOSE AN EXTRA SUBMARINE


@then("the system should not allow to have an extra submarine")
def step_impl(context):
    print(context.page.text)
    assert "Player already has a submarine" in context.page.text
    # assert context.page.status_code is 409


# PLACE A SUBMARINE


@given("the user '{username}' chose '{sub_name}' submarine")
def step_impl(context, username, sub_name):
    player = (
        context.player1 if (context.player1.username == username) else context.player2
    )
    submarines = json.load(open("app/models/underwater/options.json"))
    for key in submarines.keys():
        if submarines[key]["name"] == sub_name:
            chosen_id = key
    assert add_submarine(context.game, player.id, chosen_id)


@when(
    "the user '{username}' chooses the position '{x:d}','{y:d}' and direction '{d:d}'"
)
def step_impl(context, username, x, y, d):
    player = (
        context.player1 if (context.player1.username == username) else context.player2
    )
    submarines = context.game.submarines
    # submarine = submarines[0] if submarines[0].player_id == player.id else submarines[1]
    submarine = player.submarine[0]
    data = {
        "submarine_id": submarine.id,
        "x_coord": x,
        "y_coord": y,
        "direction": d,
    }
    context.page = context.client.post(url_for("underwater.place_submarine"), data=data)


@then("the submarine is successfully placed")
def step_impl(context):
    print(context.page.text)
    assert context.page.status_code is 200


# PLACE A SUBMARINE IN AN INVALID POSITION


@Then("the system should not allow to place the submarine in that position")
def step_impl(context):
    assert "Invalid coordinates" in context.page.text


# PLACE A SUBMARINE ALREADY PLACED


@Then("the system should not allow to place the submarine again")
def step_impl(context):
    assert "submarine is already placed" in context.page.text
