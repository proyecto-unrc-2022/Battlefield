import json

from app import db
from app.daos.navy.dynamic_missile_dao import get_missiles
from app.daos.navy.dynamic_ship_dao import execute_action, get_dynamic_ship
from app.models.navy.action_game_request import ActionGameRequest
from app.models.navy.dynamic_game import Game
from app.models.navy.dynamic_missile import DynamicMissile
from app.models.navy.dynamic_ship import DynamicShip
from app.navy.navy_constants import *
from app.navy.navy_utils import get_missile_selected, get_ship_select

data = None


def get_data():
    return data


def read_data(file_path):
    global data
    with open(file_path) as file:
        data = json.load(file)
    return data


def add_game(id_user_1, id_user_2=None):
    g = Game(id_user_1, id_user_2)
    db.session.add(g)
    db.session.commit()
    return g.id


def get_game(id_game):
    game = Game.query.filter_by(id=id_game).first()
    return game


def update_game(id_game, action: ActionGameRequest):
    global data
    if not data:
        data = read_data(PATH_TO_START)

    missiles: list[DynamicMissile] = get_missiles(id_game)
    missiles.sort(key=lambda x: x.order)
    from app.daos.navy.dynamic_missile_dao import update_missile

    for misile in missiles:
        s_misil = get_missile_selected(misile.id, data["missiles_available"])
        update_missile(misile, s_misil)

    dynamic_ship: list[DynamicShip] = get_dynamic_ship(action.id_ship, id_game)
    execute_action(dynamic_ship, action)
