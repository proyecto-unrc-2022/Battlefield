import json

from flask import url_for

from app import db
from app.daos.underwater.uw_game_dao import create_game
from app.daos.user_dao import add_user
from app.models.underwater.uw_game import UnderGame
from app.models.user import User


@given("A user is logged in")
def step_impl(context):
    add_user("test", "test", "test@example.com")
    context.user = db.session.query(User).where(User.username == "test").one_or_none()
    assert context.user


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


@given("the user {player} is logged in")
def step_impl(context, player):
    add_user(player, player, "%r@example.com" % player)
    context.visitor = (
        db.session.query(User).where(User.username == player).one_or_none()
    )
    assert context.visitor


@given("there is a game with available slots")
def step_impl(context):
    add_user("host", "host", "host@example.com")
    host = db.session.query(User).where(User.username == "host").one_or_none()
    context.game = create_game(host_id=host.id)
    assert context.game


@when("the user 'player' joins that game")
def step_impl(context):
    context.page = context.client.get(
        url_for(
            "underwater.join_game",
            game_id=context.game.id,
            visitor_id=context.visitor.id,
        )
    )
    assert context.page.status_code is 200


@then("the game is modified")
def step_impl(context):
    game = (
        db.session.query(UnderGame).where(UnderGame.id == context.game.id).one_or_none()
    )
    assert game
    assert game.visitor_id == context.visitor.id
