from behave import *
from flask import url_for


@given(u'the initialized application')
def step_impl(context):
    pass

@given(u'I have some ships available')
def step_impl(context):
    context.available_ships = {
      "ships": [
        {"type": "Destroyer", "size": 3, "velocity": 3, "hp": 60, "missile_velocity": 5, "missile_damage": 20},
        {"type": "Cruiser",  "size": 3, "velocity": 4, "hp": 70, "missile_velocity": 4, "missile_damage": 40},
        {"type": "Corvette",  "size": 2, "velocity": 4, "hp": 40, "missile_velocity": 3, "missile_damage": 15},
        {"type": "Battleship",  "size": 4, "velocity": 2, "hp": 80, "missile_velocity": 4, "missile_damage": 60}
      ]
    }
    assert context.available_ships

@when(u'we request to play a game')
def step_impl(context):
    context.page = context.client.get(url_for("navy.play"))
    assert context.page

@then(u'I should get the available ships')
def step_impl(context):
    pass
