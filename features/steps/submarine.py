import json

from flask import url_for

from app import db
from app.daos.underwater.uw_game_dao import create_game, get_game
from app.daos.user_dao import add_user
from app.models.underwater.uw_game import UnderGame
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
    assert "Saukko" in options


@given("the user {user} is logged in")
def step_impl(context, user):
    add_user(user, user, "%r@example.com" % user)
    context.user = (
        db.session.query(User).where(User.username == user).one_or_none()
    )
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


@then("the game is modified")
def step_impl(context):
    game = get_game(context.game.id)
    assert game
    assert game.visitor_id == context.user.id
