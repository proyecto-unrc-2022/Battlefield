import json

from behave import given, then, when
from flask import url_for

from app.underwater.daos.under_game_dao import game_dao


@given("there is a game of id '{id:d}' with '{username1}' and '{username2}'")
def step_impl(context, id, username1, username2):
    host = context.players[username1]
    visitor = context.players[username2]
    context.game = game_dao.create(host.id, visitor.id)
    assert context.game.host is host
    assert context.game.visitor is visitor


@given("the submarine options are the following")
def step_impl(context):
    options = json.load(open("app/underwater/options.json"))
    context.options = {}
    for row in context.table:
        context.options.update({row["name"]: row["id"]})


@when("the player asks for the submarine options")
def step_impl(context):
    context.page = context.client.get(url_for("underwater.get_options"))
    assert context.page.status_code == 200


@when(
    "the player '{username}' chooses '{sub_type}' as his submarine with position '{x:d}','{y:d}' and direction '{d:d}'"
)
def step_impl(context, username, sub_type, x, y, d):
    player = context.players[username]
    choosen_id = context.options[sub_type]
    payload = {
        "game_id": context.game.id,
        "player_id": player.id,
        "submarine_id": choosen_id,
        "x_position": x,
        "y_position": y,
        "direction": d,
    }
    context.page = context.client.post(
        url_for("underwater.choose_submarine"), data=payload
    )
