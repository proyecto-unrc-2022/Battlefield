import json

from app import db
from app.models.underwater.uw_game import UnderGame

def create_game():
    game = UnderGame()
    db.session.add(game)
    db.session.commit()
    return game
