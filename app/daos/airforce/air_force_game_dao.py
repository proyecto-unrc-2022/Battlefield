from app import db
from app.models.airforce.air_force_game import air_force_game


def add_game(player_a_id, player_b_id):
    game = air_force_game(player_a_id=player_a_id, player_b_id=player_b_id)
    db.session.add(game)
    db.session.commit()
    return game
