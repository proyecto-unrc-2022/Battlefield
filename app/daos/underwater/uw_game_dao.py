import json

from app import db
from app.models.underwater.uw_game import UnderGame
from app.models.user import User


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
