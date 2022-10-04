import json

from app import db
from app.daos.navy.dynamic_missile_dao import get_missiles, update_missile
from app.models.navy.dynamic_game import Game
from app.models.navy.dynamic_missile import DynamicMissile
from app.navy.navy_constants import *
from app.navy.navy_utils import get_missile_selected

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


def update_game(id_game):
    global data
    if not data:
        data = read_data(PATH_TO_START)

    game: Game = get_game(id_game)

    missiles: list[DynamicMissile] = game.missiles
    missiles.sort(key=lambda x: x.order)

    for misile in missiles:
        s_misil = get_missile_selected(misile.id, data["missiles_available"])
        update_missile(misile, s_misil)
