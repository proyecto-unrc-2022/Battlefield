from behave import *
from flask import url_for
from app.daos.navy.dynamic_missile_dao import add_missile, update_missile
from app.daos.navy.dynamic_ship_dao import add_ship
from app.daos.navy.game_dao import get_game
from app.daos.user_dao import add_user
from app.models.navy.dynamic_missile import DynamicMissile
from app.models.navy.dynamic_ship import DynamicShip
from app.models.user import User
from app.navy.navy_constants import EMPTY_LIST, FIRST, ONE, SECOND
from app import db
from app.navy.navy_utils import add_ship_to_map_game, get_missile_selected, get_ship_select , add_missile_to_map_game


@given("Im logged as '{user}'")
def step_impl(context,user):
    add_user(user, "12345", "user1@user1.com")
    context.user_1 = User.query.filter_by(username="user1").first()
    assert context.user_1.email == "user1@user1.com"


@given(u'the app is initialized')
def step_impl(context):
    assert context.client

@given(u'the game one is started')
def step_impl(context):
    context.headers = {"Content-Type": "application/json"}
    context.body = {"id_user_1": context.user_1.id}
    context.page = context.client.post(
        url_for("navy.create_game"), json=context.body, headers=context.headers
    )
    assert context.page 

@given(u"I have a ship '{name_ship_one}' at '{ship_one_x:d}','{ship_one_y:d}' and '{name_ship_two}' with '{hp:d}' hp at '{ship_two_x:d}','{ship_two_y:d}' on the board game")
def step_impl(context,name_ship_one,ship_one_x,ship_one_y,name_ship_two,ship_two_x,ship_two_y,hp):
    
    ship_one_selected = get_ship_select(ship_type=name_ship_one)
    ship_two_selected = get_ship_select(ship_type=name_ship_two)

    context.game_id = context.page.json["game_id"]

    ship_one = add_ship(
        id_game = context.game_id,
        id_user = context.user_1.id,
        pos_x = ship_one_x,
        pos_y = ship_one_y,
        hp=100,
        direction="N",
        ship_type=ship_one_selected['ship_id'])

    ship_two = add_ship(
        id_game = context.game_id,
        id_user = context.user_1.id,
        pos_x = ship_two_x,
        pos_y = ship_two_y,
        hp = hp,
        direction = "N",
        ship_type = ship_two_selected['ship_id']
    )

    ships_on_bd = DynamicShip.query.filter_by(id_game=context.game_id).all()
    add_ship_to_map_game(context.game_id,ships_on_bd)

    assert ship_one == ships_on_bd[FIRST]
    assert ship_two == ships_on_bd[SECOND]


@given(u"I have a missile at '{missile_x:d}','{missile_y:d}' with '{range}' range, direction '{direction}' and damage '{damage:d}'")
def step_impl(context,missile_x,missile_y,range,direction,damage):
    missile = {
        "id_game": context.game_id,
        "id_ship": 1,
        "pos_x": missile_x,
        "pos_y": missile_y,
        "order": 1,
        "direction": direction,
        "missile_type": 1
    }


    context.missile_in_game = add_missile(missile)

    add_missile_to_map_game(id_game=context.game_id, missiles=[context.missile_in_game])

    context.data_missile = {
        "speed" : int(range),
        "danger" : damage
    }
    assert context.missile_in_game    

@when(u'I move the missile')
def step_impl(context):
    update_missile(context.missile_in_game,context.data_missile)
    assert True

@then(u"I should see the missile at the new position '{missile_x:d},'{missile_y:d}'")
def step_impl(context,missile_x,missile_y):
    misil = DynamicMissile.query.filter_by(id_game=context.game_id).first()
    assert misil.pos_x == missile_x
    assert misil.pos_y == missile_y

@then(u"Missile should be destroyed")
def step_impl(context):
    misil = DynamicMissile.query.filter_by(id_game=context.game_id,id=context.missile_in_game.id).first()
    assert misil is None

@then(u"The ship at '{ship_x:d}','{ship_y:d}' should be destroyed")
def step_impl(context,ship_x,ship_y):
    ship = DynamicShip.query.filter_by(id_game=context.game_id,pos_x=ship_x,pos_y=ship_y).all()
    print(ship)

    assert ship == EMPTY_LIST

@then(u"The ship at '{ship_x:d}','{ship_y:d}' should have '{hp:d}' hp")
def step_impl(context,ship_x,ship_y,hp):
    ship : list[DynamicShip] = DynamicShip.query.filter_by(id_game=context.game_id,pos_x=ship_x,pos_y=ship_y).all()
    assert len(ship) == ONE
    assert ship[FIRST].hp == hp

@then(u"The enemy missile at '{missile_x:d}','{missile_y:d}' should be destroyed")
def step_impl(context,missile_x,missile_y):
    misil = DynamicMissile.query.filter_by(id_game=context.game_id,pos_x=missile_x,pos_y=missile_y).all()
    print("the misil is",misil)
    assert misil == EMPTY_LIST