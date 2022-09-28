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
