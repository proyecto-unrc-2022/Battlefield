from app import db
from app.daos.navy.dynamic_ship_dao import exist_ship
from app.models.navy.dynamic_game import Game
from app.models.navy.dynamic_missile import DynamicMissile
from app.navy.navy_utils import new_position, out_of_range

missiles_in_game = {}


def get_missiles(game):
    if game:
        missiles_in_game[game.id] = game.missiles
        return missiles_in_game[game.id]
    return None


def exist_missile(id_game,pos_x,pos_y):
    if not missiles_in_game[id_game]:
        return None

    missiles : list[DynamicMissile] = missiles_in_game[id_game]
    for m in missiles:
        if m.pos_x == pos_x and m.pos_y == pos_y:
            return m
    return None
            

def delete_missile(missile :DynamicMissile):
    db.session.delete(missile)
    db.session.commit()




def missil_move(missile,vel,danger):
    for i in range(vel):
        pos_x, pos_y = new_position(dir,missile.pos_x,missile.pos_y)
        if out_of_range(pos_x,pos_y):
            delete_missile(missile)
            return None
        misil_intercepted = exist_missile(missile.id_game,pos_x,pos_y)
        if misil_intercepted:
            delete_missile(misil_intercepted)
            delete_missile(missile)
            return None
        ship_intercepted = exist_ship(missile.id_game,pos_x,pos_y)
        if  ship_intercepted:
            from app.daos.navy.dynamic_ship_dao import update_hp
            update_hp(ship_intercepted,ship_intercepted.hp - danger)
            delete_missile(missile)
            return None
            
        missile.pos_x = pos_x
        missile.pos_y = pos_y
        
    return missile


def update_missile(missile : DynamicMissile,data):
    dir = missile.direction
    vel = data['speed'] #refactor
    danger = data['danger']
    missile_moved = missil_move(missile,vel,danger)
    
    if missile_moved:
        db.session.add(missile_moved)
        db.session.commit()




