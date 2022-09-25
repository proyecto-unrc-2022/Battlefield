from app import db
from app.models.navy.dynamic_game import Game



def add_game(id_user_1,id_user_2=None):
    g = Game(id_user_1,id_user_2)
    db.session.add(g)
    db.session.commit()
    return g.id

