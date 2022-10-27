import json

from behave import *

from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.ship_service import ship_service


@when("The ship with id '{id:d}' turns to '{course}'")
def step_impl(context, id, course):
    navy_game_service.load_game(context.game.id)
    ship = ship_service.get_by_id(id)
    ship_service.turn(ship, course)


@then("I should see the ship '{id:d}' with the new course '{course}'")
def step_impl(context, id, course):
    ship = ship_service.get_by_id(id)
    assert ship.course == course


@then("The ship with id '{id:d}' should have '{hp:d}' hp")
def step_impl(context, id, hp):
    ship = ship_service.get_by_id(id)
    assert ship.hp == hp


@then("The ship with id '{id:d}' should be destroyed")
def step_impl(context, id):
    ship = ship_service.get_by_id(id)
    print(ship)
    assert ship is None
