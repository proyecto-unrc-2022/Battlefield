import json

from behave import *
from flask import url_for

from app import db
from app.daos.navy.game_dao import add_game, get_game, read_data
from app.daos.user_dao import add_user
from app.models.navy.dynamic_game import Game
from app.models.user import User
from app.navy.navy_constants import PATH_TO_START
from app.navy.navy_utils import check_dynamic_data


@given('I am logged in as "user1"')
def step_impl(context):
    # Falta hacer el login y obtener el token
    add_user("user1", "12345", "user1@user1.com")
    context.user_1 = User.query.filter_by(username="user1").first()
    assert context.user_1.email == "user1@user1.com"


@given("the app has been initialized")
def step_impl(context):
    assert context.client


@given("I have some ships available")
def step_impl(context):
    context.available_ships = read_data(PATH_TO_START)
    assert context.available_ships


@when("I request to create a game")
def step_impl(context):
    context.headers = {"Content-Type": "application/json"}
    context.body = {"id_user_1": context.user_1.id}
    context.page = context.client.post(
        url_for("navy.create_game"), json=context.body, headers=context.headers
    )
    assert context.page


@then("I should get the available ships and the game id")
def step_impl(context):
    data = json.loads(context.page.text)
    ships = context.available_ships
    ships["game_id"] = Game.query.filter_by(id_user_1=context.user_1.id).first().id

    assert data == ships


@given("I have a game created")
def step_impl(context):
    context.game_id = add_game(context.user_1.id)
    assert context.game_id


@given("I have ships to choose")
def step_impl(context):
    context.available_ships = read_data(PATH_TO_START)
    assert context.available_ships


@when(
    "I choose a '{ship_type}' ship in ('{pos_x}', '{pos_y}') position, and '{bow_dir}' direction"
)
def step_impl(context, ship_type, pos_x, pos_y, bow_dir):
    ship_selected = None
    for ship in context.available_ships["ships_available"]:
        if ship["name"] == ship_type:
            ship_selected = ship

    context.data = {
        "game_id": context.game_id,
        "id_user_1": context.user_1.id,
        "hp": ship_selected["hp"],
        "direction": bow_dir,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "ship_type": ship_selected["ship_id"],
    }

    context.headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("navy.start_game"), json=context.data, headers=context.headers
    )

    assert context.page


@then(
    "I should see the game board, with the ship located in ('2', '3') and directed to 'N'"
)
def step_impl(context):
    data = json.loads(context.page.data)
    assert check_dynamic_data(data, 2, 3, "N")
