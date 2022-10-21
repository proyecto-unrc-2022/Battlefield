import json

from behave import *
from app.navy.models.action import Action
from app.navy.services.navy_game_service import navy_game_service
from steps.navy.test_utils import test_utils
from app.navy.services.ship_service import ship_service

@then(u"I should see the ship at the new position '{pos_x:d}','{pos_y:d}'")
def step_impl(context, pos_x, pos_y):
    ship = navy_game_service.get_from_map(context.game.id, pos_x, pos_y)
    assert ship == context.ship
    assert context.ship.pos_x == pos_x
    assert context.ship.pos_y == pos_y

@when(u"The ship moves '{x}' positions")
def step_impl(context, x):
    navy_game_service.load_game_to_map(context.game.id)

    action = test_utils.add_action_test(context.game.id, context.ship.id, context.ship.course, x, 0, context.ship.missile_type_id, context.user1.id)
    ship_service.move(context.ship, action)
