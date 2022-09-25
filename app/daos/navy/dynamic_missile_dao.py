from app import db
from app.models.navy.dynamic_missile import DynamicMissile


def get_missiles(id_game=None):
    if id_game:
        return DynamicMissile.query.filter_by(id_game=id_game).all()
    return DynamicMissile.query.all()
