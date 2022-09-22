from flask import url_for
import json

from app import db
from app.models.underwater.uw_game import UnderGame
from app.models.user import User
from app.daos.user_dao import add_user

@given(u'A user is logged in')
def step_impl(context):
    add_user("test", "test", "test@example.com")
    context.user = db.session.query(User).where(User.username=="test").one_or_none()
    assert context.user

@when(u'the user asks for a new underwater game')
def step_impl(context):
    context.page = context.client.get(url_for("underwater.new_game", host_id=context.user.id))
    assert context.page

@then(u'A new game is registered')
def step_impl(context):
    data = json.loads(context.page.text)
    game = db.session.query(UnderGame).filter_by(id=data['game_id']).first()
    assert game

@then(u'an empty board with one player is returned')
def step_impl(context):
    pass


@given(u'the system is running')
def step_impl(context):
    pass


@when(u'I receive a request to show the submarine options')
def step_impl(context):
    context.page = context.client.get(url_for("underwater.get_options"))
    assert context.page


@then(u'the options are returned')
def step_impl(context):
    options = json.loads(context.page.text)
    assert "Saukko" in options
