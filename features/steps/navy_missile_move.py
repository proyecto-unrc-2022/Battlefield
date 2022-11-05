import json

from behave import *
from flask import url_for
from steps.navy.test_utils import test_utils


@given("the app is initialized")
def step_impl(context):
    context.token = json.loads(context.page.text)
    assert context.token


@given("the game is started")
def step_impl(context):

    from app.navy.services.navy_game_service import navy_game_service

    context.game = navy_game_service.add({"user1_id": context.user1.id})
    context.game = navy_game_service.join_second_player(
        {"user2_id": context.user2.id}, context.game.id
    )
    assert context.game


@given(
    "The user '{id:d}' has a ship '{ship_name}' in '{pos_x:d}','{pos_y:d}' with course '{course}' and hp '{hp:d}'"
)
def step_impl(context, ship_name, pos_x, pos_y, course, hp, id):
    context.ship = test_utils.add_test_ship(
        name=ship_name,
        pos_x=pos_x,
        pos_y=pos_y,
        course=course,
        hp=hp,
        navy_game_id=context.game.id,
        user_id=id,
    )

    from app.navy.services.ship_service import ship_service

    ships_db = ship_service.get_by(navy_game_id=context.game.id)
    assert context.ship in ships_db


@given(
    "There is a missile at '{pos_x:d}','{pos_y:d}' with speed '{speed:d}', course '{course}' and damage '{damage:d}'"
)
def step_impl(context, pos_x, pos_y, speed, course, damage):
    context.missile_test = test_utils.add_test_missile(
        pos_x=pos_x,
        pos_y=pos_y,
        speed=speed,
        course=course,
        damage=damage,
        navy_game_id=context.game.id,
        ship_id=context.ship.id,
        missile_type=context.ship.missile_type_id,
    )

    from app.navy.services.missile_service import missile_service

    missiles_db = missile_service.get(navy_game_id=context.game.id)
    assert context.missile_test in missiles_db


@when("The missile moves")
def step_impl(context):
    from app.navy.services.missile_service import missile_service
    from app.navy.services.navy_game_service import navy_game_service

    navy_game_service.load_game(context.game.id)
    old_x, old_y = context.missile_test.pos_x, context.missile_test.pos_y
    missile_service.update_position(context.missile_test)
    assert not navy_game_service.get_from_board(context.game.id, old_x, old_y)


@then("I should see the missile at the new position '{pos_x:d}','{pos_y:d}'")
def step_impl(context, pos_x, pos_y):
    from app.navy.services.navy_game_service import navy_game_service

    missile = navy_game_service.get_from_board(context.game.id, pos_x, pos_y)
    assert missile == context.missile_test


@then("Missile should be destroyed")
def step_impl(context):
    from app.navy.daos.missile_dao import missile_dao

    missile = missile_dao.get_by_id(context.missile_test.id)
    assert not missile.is_alive


@then("The ship at '{pos_x:d}','{pos_y:d}' should be destroyed")
def step_impl(context, pos_x, pos_y):
    from app.navy.daos.ship_dao import ship_dao
    from app.navy.services.navy_game_service import navy_game_service

    ship_map = navy_game_service.get_from_board(context.game.id, pos_x, pos_y)
    ship_bd = ship_dao.get_by_id(context.ship.id)
    assert ship_map is None and not ship_bd.is_alive


@then("The ship at '{pos_x:d}','{pos_y:d}' should have '{hp:d}' hp")
def step_impl(context, pos_x, pos_y, hp):
    from app.navy.daos.ship_dao import ship_dao
    from app.navy.services.navy_game_service import navy_game_service

    ship_bd = ship_dao.get_by_id(context.ship.id)
    ship = navy_game_service.get_ship_from_game(context.game.id, context.ship.id)
    assert ship.pos_x == pos_x and ship.pos_y == pos_y and ship.hp == hp
    assert ship_bd.pos_x == pos_x and ship_bd.pos_y == pos_y and ship_bd.hp == hp
