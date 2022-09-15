from behave import *
from flask import url_for
import json
from app.navy.game import Game

@given(u'the initialized application')
def step_impl(context):
    pass

@given(u'I have some ships available')
def step_impl(context):
    context.available_ships = Game.read_data("app/navy/start.json")
    assert context.available_ships

@when(u'I request to play a game')
def step_impl(context):
    context.page = context.client.get(url_for("navy.play"))
    assert context.page

@then(u'I should get the available ships')
def step_impl(context):
    data = json.loads(context.page.text)
    ships = context.available_ships 

    assert 'ships_available' in data 
    assert len(data['ships_available']) == len(ships['ships_available'])
    

