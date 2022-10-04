from flask import jsonify

from app.models.navy.dynamic_missile import DynamicMissile
from app.navy.navy_constants import BORDERS, COORDS, XCORD, YCORD


def check_dynamic_data(data, pos_x, pos_y, dir):
    return (
        data["data"]["dynamic_data"]["ships"][0]["pos_x"] == pos_x
        and data["data"]["dynamic_data"]["ships"][0]["pos_y"] == pos_y
        and data["data"]["dynamic_data"]["ships"][0]["direction"] == dir
    )


def get_ship_select(ships, ship_type):
    for ship in ships:
        if ship["name"] == ship_type:
            return ship
    return None

def get_missile_selected(misiles,id_misil):
    for m in misiles: 
        if m['missile_id'] == id_misil:
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
    return pos_x < BORDERS['top'] or pos_x > BORDERS['bottom'] or pos_y < BORDERS['left'] or pos_y > BORDERS['right']


def json_selected_options(game_id, id_user_1, direction, pos_x, pos_y, ship_selected):
    return {
        "game_id": game_id,
        "id_user": id_user_1,
        "direction": direction,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "ship_type": ship_selected["ship_id"],
    }
