import json

from app import db
from app.models.underwater.under_dtos import UnderGame
from app.models.user import User

from .submarine_dao import create_submarine


def create_game(host_id):
    if db.session.query(User).where(User.id == host_id) == None:
        return None

    game = UnderGame(host_id=host_id)
    db.session.add(game)
    db.session.commit()
    return game


def get_game(game_id):
    game = db.session.query(UnderGame).where(UnderGame.id == game_id).one_or_none()
    return game


def update_game(game_id, host_id=None, visitor_id=None):
    game = get_game(game_id)
    if not game:
        return None
    if host_id != None:
        game.host_id = host_id
    if visitor_id != None:
        game.visitor_id = visitor_id

    db.session.commit()
    return game


def get_options():
    options_json = open("app/models/underwater/options.json")
    options = json.load(options_json)
    return options


def add_submarine(game, player_id, option_id):
    options = get_options()
    choosen = options[option_id]
    sub = create_submarine(
        game.id,
        player_id,
        choosen["name"],
        int(choosen["size"]),
        int(choosen["speed"]),
        int(choosen["visibility"]),
        int(choosen["radar_scope"]),
        float(choosen["health"]),
        int(choosen["torpedo_speed"]),
        float(choosen["torpedo_damage"]),
    )
    game.submarines.append(sub)
    db.session.commit()
    return sub
