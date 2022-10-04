from app import db
from app.models.navy.dynamic_ship import DynamicShip
from app.navy.navy_utils import get_ship_selected_by_id
from app.daos.navy.game_dao import read_data
from app.navy.navy_constants import PATH_TO_START


def add_ship(data):
    ships = read_data(PATH_TO_START)['ships_available']
    ship_selected = get_ship_selected_by_id(ships, data['ship_type'])
    dynamicShip = DynamicShip(
        id_game=data['game_id'],
        id_user=data['id_user'],
        hp=ship_selected['hp'],
        direction=data['direction'],
        pos_x=data['pos_x'],
        pos_y=data['pos_y'],
        ship_type=data['ship_type'],
    )
    db.session.add(dynamicShip)
    db.session.commit()


def get_ships(id_game=None):
    if id_game:
        return DynamicShip.query.filter_by(id_game=id_game).all()
    return DynamicShip.query.all()
