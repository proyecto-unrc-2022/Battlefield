from app import db
from app.daos.navy.dynamic_ship_dao import exist_ship
from app.models.navy.dynamic_game import Game
from app.models.navy.dynamic_missile import DynamicMissile
from app.navy.navy_utils import new_position, out_of_range

missiles_in_game = {}


def add_missile(data):
    missile = DynamicMissile(**data)
    db.session.add(missile)
    db.session.commit()
    return missile


def set_missile_in_game(id_game, missiles):
    missiles_in_game[id_game] = missiles


def get_missiles(id_game):
    if id_game:
        missiles_in_game[id_game] = DynamicMissile.query.filter_by(
            id_game=id_game
        ).all()
        return missiles_in_game[id_game]
    return DynamicMissile.query.all()


def exist_missile(id_game, pos_x, pos_y):
    if not missiles_in_game[id_game]:
        return None

    missiles: list[DynamicMissile] = missiles_in_game[id_game]
    for m in missiles:
        if m.pos_x == pos_x and m.pos_y == pos_y:
            return m
    return None


def delete_missile(missile: DynamicMissile):
    db.session.delete(missile)
    db.session.commit()


def missil_move(missile, vel, danger, dir):
    for i in range(vel):
        pos_x, pos_y = new_position(dir, missile.pos_x, missile.pos_y)
        if out_of_range(pos_x, pos_y):
            delete_missile(missile)
            return None
        misil_intercepted = exist_missile(missile.id_game, pos_x, pos_y)
        if misil_intercepted:
            delete_missile(misil_intercepted)
            delete_missile(missile)
            return None
        ship_intercepted = exist_ship(missile.id_game, pos_x, pos_y)
        if ship_intercepted:
            from app.daos.navy.dynamic_ship_dao import update_hp

            update_hp(ship=ship_intercepted, new_hp=ship_intercepted.hp - danger)
            delete_missile(missile)
            return None

        missile.pos_x = pos_x
        missile.pos_y = pos_y

    return missile


def update_missile(missile :DynamicMissile, data):
    print(missile)
    dir = missile.direction
    vel = data["speed"]  # refactor
    danger = data["danger"]
    missile_moved = missil_move(missile, vel, danger, dir)

    if missile_moved:
        db.session.add(missile_moved)
        db.session.commit()
