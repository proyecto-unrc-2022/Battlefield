from app import db
from app.models.navy.dynamic_ship import DynamicShip


def add_ship(id_game, id_user, hp, direction, pos_x, pos_y, ship_type):
    dynamicShip = DynamicShip(
        id_game=id_game,
        id_user=id_user,
        hp=hp,
        direction=direction,
        pos_x=pos_x,
        pos_y=pos_y,
        ship_type=ship_type,
    )
    db.session.add(dynamicShip)
    db.session.commit()


def get_ships(id_game=None):
    if id_game:
        return DynamicShip.query.filter_by(id_game=id_game).all()
    return DynamicShip.query.all()
