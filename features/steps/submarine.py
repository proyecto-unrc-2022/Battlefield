import json

from flask import url_for

from app import db
from app.daos.underwater.uw_game_dao import (
    add_submarine,
    create_game,
    get_game,
    update_game,
)
from app.daos.user_dao import add_user
from app.models.underwater.under_models import UnderGame
from app.models.user import User


@when("the user asks for a new underwater game")
def step_impl(context):
    context.page = context.client.get(
        url_for("underwater.new_game", host_id=context.user.id)
    )
    assert context.page


@then("A new game is registered")
def step_impl(context):
    data = json.loads(context.page.text)
    game = db.session.query(UnderGame).filter_by(id=data["id"]).first()
    assert game


@then("an empty board with one player is returned")
def step_impl(context):
    pass


@given("the system is running")
def step_impl(context):
    pass


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


@given("the user {user} is logged in")
def step_impl(context, user):
    add_user(user, user, "%r@example.com" % user)
    context.user = db.session.query(User).where(User.username == user).one_or_none()
    assert context.user


@given("there is a game with available slots")
def step_impl(context):
    add_user("host", "host", "host@example.com")
    host = db.session.query(User).where(User.username == "host").one_or_none()
    context.game = create_game(host_id=host.id)
    assert context.game


@when("the user {user} joins that game")
def step_impl(context, user):
    context.page = context.client.get(
        url_for(
            "underwater.join_game",
            game_id=context.game.id,
            visitor_id=context.user.id,
        )
    )
    assert context.page.status_code is 200


@then("the game now has the new visitor")
def step_impl(context):
    game = get_game(context.game.id)
    assert game
    assert game.visitor_id == context.user.id


@given("the user is in an ongoing game")
def step_impl(context):
    add_user("visitor", "visitor", "visitor@example.com")
    visitor = db.session.query(User).where(User.username == "visitor").one_or_none()

    game = create_game(host_id=context.user.id)
    context.game = update_game(game_id=game.id, visitor_id=visitor.id)
    assert context.game


@when("the user chooses a submarine")
def step_impl(context):
    data = {"game_id": context.game.id, "player_id": context.user.id, "submarine_id": 1}
    context.page = context.client.post(
        url_for("underwater.choose_submarine"), data=data
    )
    assert context.page.status_code is 200


@then("the game bounds the user to the choosen submarine")
def step_impl(context):
    game = get_game(context.game.id)
    print(game.submarines[0].player_id)
    assert game.submarines[0].player_id == context.user.id


@given("they chose '{sub_name}' submarine")
def step_impl(context, sub_name):
    submarines = json.load(open("app/models/underwater/options.json"))
    for key in submarines.keys():
        if submarines[key]["name"] == sub_name:
            chosen_id = key
    add_submarine(context.game, context.user.id, chosen_id)


@when("they choose the position '{x:d}','{y:d}','{d:d}' for their submarine")
def step_impl(context, x, y, d):
    data = {
        "submarine_id": context.game.submarines[0].id,
        "x_coord": x,
        "y_coord": y,
        "direction": d,
    }
    context.page = context.client.post(url_for("underwater.place_submarine"), data=data)


@then("the submarine is successfully placed")
def step_impl(context):
    print(context.page.text)
    assert context.page.status_code is 200
