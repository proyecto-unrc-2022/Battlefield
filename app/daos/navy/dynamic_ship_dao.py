from app import db
from app.daos.navy.dynamic_missile_dao import delete_missile, exist_missile
from app.models.navy.dynamic_ship import DynamicShip
from app.navy.navy_constants import FIRST, INV_DIR, MINIMUM_HP, PATH_TO_START
from app.navy.navy_utils import (
    get_ship_select,
    get_ship_select_by_id,
    get_ship_selected_by_id,
    new_position,
)

ships_in_game = {}


def set_ships_in_game(id_game, ships):
    ships_in_game[id_game] = ships


def add_ship(data):
    from app.daos.navy.game_dao import read_data

    ships = read_data(PATH_TO_START)["ships_available"]
    ship_selected = get_ship_selected_by_id(ships, data["ship_type"])
    dynamicShip = DynamicShip(
        id_game=data["game_id"],
        id_user=data["id_user"],
        hp=ship_selected["hp"],
        direction=data["direction"],
        pos_x=data["pos_x"],
        pos_y=data["pos_y"],
        ship_type=data["ship_type"],
    )
    db.session.add(dynamicShip)
    db.session.commit()


def re_build(dir, pos_x, pos_y, ship_type):
    ship = get_ship_select_by_id(ship_type)
    occupied_positions = [(pos_x, pos_y)]
    print(occupied_positions)

    tail_dir = INV_DIR[dir]
    for i in range(FIRST, ship["size"] - 1):
        pos_x, pos_y = new_position(tail_dir, pos_x, pos_y)
        occupied_positions.append((pos_x, pos_y))
    print(occupied_positions)
    return occupied_positions


def exist_ship(id_game, pos_x, pos_y):
    ships = ships_in_game[id_game]
    for ship in ships:
        temp_size = re_build(ship.direction, ship.pos_x, ship.pos_y, ship.ship_type)
        if (pos_x, pos_y) in temp_size:
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


def get_dynamic_ship(id_ship, id_game):
    return DynamicShip.query.filter_by(id_game=id_game, id=id_ship).one_or_none()


def can_twist(ship, dir):
    pass


def execute_action(ship, action):
    ship.dir = action.dir
    occupied_positions = re_build(ship)
    # Twist
    for position in occupied_positions:
        x, y = position
        missile = exist_missile(ship.id_game, x, y)
        if missile:
            update_hp(ship.hp - missile.danger, ship)
            delete_missile(missile)

        other_ship = exist_ship(ship.id_game, x, y)
        if other_ship:
            if ship.hp > other_ship.hp:
                update_hp(ship.hp - other_ship.hp, ship)
                delete_ship(other_ship)
            else:
                update_hp(other_ship.hp - ship.hp, other_ship)
                delete_ship(ship)
            return None

    if action.attack:
        pass
    else:
        for i in range(action.move):
            pos_x, pos_y = new_position(dir, ship.pos_x, ship.pos_y)

            missile = exist_missile(ship.id_game, pos_x, pos_y)
            if missile:
                update_hp(ship.hp - missile.danger, ship)
                delete_missile(missile)
            other_ship = exist_ship(missile.id_game, pos_x, pos_y)
            if other_ship:
                if ship.hp > other_ship.hp:
                    update_hp(ship.hp - other_ship.hp, ship)
                    delete_ship(other_ship)
                else:
                    update_hp(other_ship.hp - ship.hp, other_ship)
                    delete_ship(ship)
                return None

            ship.pos_x = pos_x
            ship.pos_y = pos_y
