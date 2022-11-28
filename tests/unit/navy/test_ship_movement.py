import pytest

from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.ship_service import ship_service
from battlefield import app
from features.steps.navy.test_utils import test_utils


def test_ship_turn_without_collision(arrange_navy_game):
    navy_game_service.load_game(1)
    ship = test_utils.add_test_ship("Destroyer", 5, 4, "W", 1, 1, 60, 3, 3, 5, 1)

    ship_service.turn(ship, "E")
    ship_service.update_position(ship, 0)

    game = navy_game_service.get_board(1)
    assert game[(ship.pos_x, ship.pos_y)].course == "E"


def test_ship_turn_missile_collision(arrange_navy_game):
    navy_game_service.load_game(1)
    ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 60, 3, 3, 5, 1)
    missile = test_utils.add_test_missile("W", "5", "7", 1, 1, 1, 30, 1)
    ship_service.turn(ship, "W")
    ship_service.update_position(ship, 0)

    game = navy_game_service.get_board(1)
    assert game[(ship.pos_x, ship.pos_y)].course == "W"
    assert game[(ship.pos_x, ship.pos_y)].hp == "30"
