import json

from app import db
from app.models.navy.dynamic_game import Game


def read_data(file_path):
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
