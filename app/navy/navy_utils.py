from flask import jsonify
from app import db
from app.models.navy.dynamic_ship import DynamicShip
from app.navy.navy_constants import BORDERS, COORDS, PATH_TO_START, XCORD, YCORD
from app.navy.navy_constants import PATH_TO_START


def check_dynamic_data(data, pos_x, pos_y, dir):
    return (
        data["data"]["dynamic_data"]["ships"][0]["pos_x"] == pos_x
        and data["data"]["dynamic_data"]["ships"][0]["pos_y"] == pos_y
        and data["data"]["dynamic_data"]["ships"][0]["direction"] == dir
    )


def get_ship_select(ships=None, ship_type=None):
    from app.daos.navy.game_dao import read_data

    if not ships:
        ships = read_data(PATH_TO_START)["ships_available"]

    for ship in ships:
        if ship["name"] == ship_type:
            return ship
    return None

def get_ship_selected_by_id(ships,ship_id):
    for ship in ships:
        if ship["ship_id"] == ship_id:
            return ship
    return None

def add_ship_special(
    id_game,
    id_user,
    pos_x,
    pos_y,
    hp,
    direction,
    ship_type
    ):
    ship = DynamicShip(
        id_game = id_game,
        id_user = id_user,
        pos_x = pos_x,
        pos_y = pos_y,
        hp = hp,
        direction = direction,
        ship_type = ship_type
    )
    db.session.add(ship)
    db.session.commit()

    return ship



def get_ship_select_by_id(id_ship, ships=None):
    from app.daos.navy.game_dao import read_data

    if not ships:
        ships = read_data(PATH_TO_START)["ships_available"]
    for ship in ships:
        if ship["ship_id"] == id_ship:
            return ship
    return None


def get_missile_selected(id_misil, misiles=None):
    if misiles is None:
        from app.daos.navy.game_dao import read_data

        misiles = read_data(PATH_TO_START)["missiles_available"]
    for m in misiles:
        if m["missile_id"] == id_misil:
            return m
    return None


def get_ship_selected_by_id(ships, ship_id):

    for ship in ships:
        if ship["ship_id"] == ship_id:
            return ship

    return None

def new_position(dir,pos_x, pos_y):
    if dir in COORDS:
        return (pos_x + COORDS[dir][XCORD], pos_y + COORDS[dir][YCORD])
    return None


def out_of_range(pos_x, pos_y):
    return (
        pos_x < BORDERS["top"]
        or pos_x > BORDERS["bottom"]
        or pos_y < BORDERS["left"]
        or pos_y > BORDERS["right"]
    )


def get_move_ship_(ship_type):
    from app.daos.navy.game_dao import read_data
    ships = read_data(PATH_TO_START)
    for ship in ships["ships_available"]:
        if ship["ship_id"] == ship_type:
            return ship["speed"]

    return None


def json_selected_options(game_id, id_user_1, direction, pos_x, pos_y, ship_selected):
    return {
        "game_id": game_id,
        "id_user": id_user_1,
        "direction": direction,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "ship_type": ship_selected["ship_id"],
    }


# MISSILES TEST-CHEAT FUNCTIONS
def add_missile_to_map_game(id_game, missiles):
    from app.daos.navy.dynamic_missile_dao import set_missile_in_game

    set_missile_in_game(id_game, missiles)


# SHIPS TEST-CHEAT FUNCTIONS
def add_ship_to_map_game(id_game, ships):
    from app.daos.navy.dynamic_ship_dao import set_ships_in_game

    set_ships_in_game(id_game, ships)
