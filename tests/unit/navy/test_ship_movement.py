import pytest
from features.steps.navy.test_utils import test_utils

def test_move(arrange_navy_game):
    from app.navy.services.ship_service import ship_service
    
    ship1 = {"name": "Destroyer", "hp": 60, "size": 3, "speed": 3, "visibility": 5, "missile_type_id": 1, "pos_x": 5, "pos_y": 4, "course": "W", "user_id": 1, "navy_game_id": 1}  
    ship_service.add(ship1)
    ship = ship_service.get_by_id(1)
    
    action1 = test_utils.add_action_test(1, 1, "W", 2, 0, 1, 1, 1)
    ship_service.update_position(ship, action1.move)
    
    assert ship.pos_x == 5 and ship.pos_y == 2