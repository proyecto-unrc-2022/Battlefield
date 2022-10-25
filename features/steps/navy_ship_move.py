import json

from behave import *
from app.navy.models.action import Action
from app.navy.services.navy_game_service import navy_game_service
from steps.navy.test_utils import test_utils
from app.navy.services.ship_service import ship_service

@then(u"I should see the ship at the position '{pos_x:d}','{pos_y:d}'")
def step_impl(context, pos_x, pos_y):
    ship = navy_game_service.get_from_board(context.game.id, pos_x, pos_y)
    ship1 = ship_service.get_by_id(1)
    print(navy_game_service.games[1])
    assert ship == ship1
    assert ship1.pos_x == pos_x
    assert ship1.pos_y == pos_y

@when(u"The ship id '{id:d}' moves '{x}' positions")
def step_impl(context, id, x):
    navy_game_service.load_game(context.game.id)
    ship1 = ship_service.get_by_id(id)
    action = test_utils.add_action_test(context.game.id, ship1.id, ship1.course, x, 0, ship1.missile_type_id, context.user1.id)
    ship_service.update_position(ship1, action)
