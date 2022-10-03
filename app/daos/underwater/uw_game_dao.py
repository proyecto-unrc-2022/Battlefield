import json

import app.daos.underwater.submarine_dao as sub_dao
from app import db
from app.models.underwater.under_dtos import UnderGame
from app.models.underwater.under_models import UnderBoard, boards
from app.daos.underwater.submarine_dao import is_placed, update_position
from app.models.user import User


def create_game(host_id, height=10, width=20):
    if db.session.query(User).where(User.id == host_id) == None:
        return None

    game = UnderGame(host_id=host_id)
    db.session.add(game)
    db.session.commit()
    boards.update({game.id: UnderBoard(game.id, height, width)})
    return game


def get_game(game_id):
    game = db.session.query(UnderGame).where(UnderGame.id == game_id).one_or_none()
    return game


def update_game(game_id, host_id=None, visitor_id=None):
    game = get_game(game_id)
    if not game:
        return None
    if host_id != None:
        game.host_id = host_id
    if visitor_id != None:
        game.visitor_id = visitor_id

    db.session.commit()
    return game


def get_options():
    options_json = open("app/models/underwater/options.json")
    options = json.load(options_json)
    return options


def add_submarine(game, player_id, option_id):
    options = get_options()
    choosen = options[str(option_id)]

    if not has_user(game, player_id):
        raise Exception("the game does not have the specified player")

    for sub in game.submarines:
        if sub.player_id == player_id:
            raise Exception("Player already has a submarine")

    sub = sub_dao.create_submarine(
        game.id,
        player_id,
        choosen["name"],
        int(choosen["size"]),
        int(choosen["speed"]),
        int(choosen["visibility"]),
        int(choosen["radar_scope"]),
        float(choosen["health"]),
        int(choosen["torpedo_speed"]),
        float(choosen["torpedo_damage"]),
    )
    game.submarines.append(sub)
    db.session.commit()
    return sub


def has_user(game, player_id):
    return game.host_id == player_id or game.visitor_id == player_id


def place_submarine(submarine, x_coord, y_coord, direction):
    if is_placed(submarine):
        raise Exception("submarine is already placed")

    board = boards[submarine.game.id]

    # if not board.segment_is_empty(x_coord, y_coord, direction, submarine.size):
    #     raise Exception("Given position is not available")
    try:
        board.place(submarine, x_coord, y_coord, direction, submarine.size)
    except Exception as e:
        raise Exception("%s" % str(e))

    update_position(submarine, x_coord, y_coord, direction)

    db.session.commit()


def contains_submarine(game, submarine_id):
    for sub in game.submarines:
        if sub.id == submarine_id:
            return True
    return False
