from flask import url_for
import json

from app import db
from app.models.underwater.uw_game import UnderGame

@given(u'A user is logged in')
def step_impl(context):
    pass

@when(u'the user asks for a new underwater game')
def step_impl(context):
    context.page = context.client.get(url_for("underwater.new_game"))
    assert context.page

@then(u'A new game is registered')
def step_impl(context):
    data = json.loads(context.page.text)
    game = db.session.query(UnderGame).filter_by(id=data['game_id']).first()
    assert game

@then(u'an empty board with one player is returned')
def step_impl(context):
    pass
