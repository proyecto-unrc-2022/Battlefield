from app import db
from ...models.navy.dynamic_navy_models import Game


def add_game(id_user_1,id_user_2=None):
    g = Game(id_user_1,id_user_2)
    db.session.add(g)
    db.session.commit()
    return g.id
