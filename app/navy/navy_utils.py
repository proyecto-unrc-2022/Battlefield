from flask import jsonify


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


def json_selected_options(game_id, id_user_1, direction, pos_x, pos_y, ship_selected):
    return {
        "game_id": game_id,
        "id_user_1": id_user_1,
        "hp": ship_selected["hp"],
        "direction": direction,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "ship_type": ship_selected["ship_id"],
    }
