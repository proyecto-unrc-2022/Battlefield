from app import db
from app.models.navy.dynamic_ship import DynamicShip
from app.navy.navy_constants import MINIMUM_HP
from app.navy.navy_utils import get_ship_select, new_position
ships_in_game = {}

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

def re_build(dir,pos_x,pos_y,ship_type):
    from app.daos.navy.game_dao import get_data
    ship = get_ship_select(get_data()['ships_available'],ship_type)
    occupied_positions = [(pos_x,pos_y)]

    for i in range(ship['size']-1):
         occupied_positions.append(new_position(dir,pos_x,pos_y))
    return occupied_positions

def exist_ship(id_game,pos_x,pos_y):
    ships :list[DynamicShip]= ships_in_game[id_game]
    for ship in ships:
       ship['occupied_positions'] = re_build(ship.direction,ship.pos_x,ship.pos_y,ship.ship_type)
       if (pos_x,pos_y) in ship['occupied_positions']:
            return ship    
    return None


def delete_ship(ship):
    db.session.delete(ship)
    db.session.commit()


def update_hp(new_hp, ship):
    if new_hp <= MINIMUM_HP:
        delete_ship(ship)
    else:
        ship.hp = new_hp
        db.session.add(ship)
        db.session.commit()            

def get_ships(id_game=None):
    if id_game:
        ships_in_game[id_game] = DynamicShip.query.filter_by(id_game=id_game).all()
        return ships_in_game[id_game]
    return None

