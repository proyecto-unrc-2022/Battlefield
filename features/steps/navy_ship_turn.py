import json

from behave import *
from flask import url_for

from app.navy.services.ship_service import ship_service


@when("The ship with id '{id:d}' turns to '{course}'")
def step_impl(context, id, course):
    pass


@then("I should see the ship with the new course '{course}'")
def step_impl(context, course):
    pass


@then("The ship with id '{id:d}' should have '{hp:d}' hp")
def step_impl(context, id, hp):
    ship = ship_service.get_by_id(id)
    assert ship.hp == hp


@then("The ship with id '{id:d}' should be destroyed")
def step_impl(context, id):
    ship = ship_service.get_by_id(id)
    assert ship.hp <= 0


@then(
    "Only the '{pos_x:d}','{pos_y:d}' position should be visible for the ship '{id:d}'"
)
def step_impl(context, pos_x, pos_y, id):
    pass
