from behave import *
from steps.navy.test_utils import test_utils


@given(
    "a missile exists from user '{user_id:d}' in '{pos_x:d}', '{pos_y:d}' with course '{course}', speed '{speed:d}', and damage '{damage:d}' in the NavyGame '{game_id:d}'"
)
def step_impl(context, user_id, pos_x, pos_y, course, speed, damage, game_id):
    from app.navy.services.missile_service import missile_service

    missile_db = test_utils.add_test_missile(
        course,
        pos_x,
        pos_y,
        context.ships[user_id].id,
        game_id,
        context.ships[user_id].missile_type_id,
        damage,
        speed,
    )

    try:
        context.missiles[game_id].append(missile_db)
    except:
        context.missiles = {}
        context.missiles[game_id] = []
        context.missiles[game_id].append(missile_db)

    missiles_db = missile_service.get(navy_game_id=game_id)
    assert missile_db in missiles_db


@then(
    "a missile with course '{course}', speed '{speed:d}', and damage '{damage:d}' should be in '{pos_x:d}', '{pos_y:d}' in the NavyGame '{game_id:d}'"
)
def step_impl(context, course, speed, damage, pos_x, pos_y, game_id):
    from app.navy.services.navy_game_service import navy_game_service

    missile = navy_game_service.get_from_board(game_id, pos_x, pos_y)

    assert missile.course == course
    assert missile.speed == speed
    assert missile.damage == damage


@then("the missile '{missile_id:d}' in NavyGame '{game_id:d}' should be destroyed")
def step_impl(context, missile_id, game_id):
    filtered_missile = filter(lambda x: x.id == missile_id, context.missiles[game_id])
    assert not list(filtered_missile)[0].is_alive
