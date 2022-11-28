from battlefield import app
from features.steps.navy.test_utils import test_utils
from app.navy.services.ship_service import ship_service
from app.navy.services.navy_game_service import navy_game_service
from app.navy.services.missile_service import missile_service

def test_missile_move_without_collision():
    with app.app_context():
        #Arrange
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 30, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("E", 5, 5, 1, 1, 1, 50, 2)
        navy_game_service.load_game(1)
        
        #Act
        missile_service.update_position(missile)
        
        #Assert
        missile = navy_game_service.get_missiles(1)[0]
        assert missile.pos_x == 5 and missile.pos_y == 7
        
        
def test_missile_move_right_border():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 30, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("E", 5, 20, 1, 1, 1, 50, 2)
        navy_game_service.load_game(1)
        
        missile_service.update_position(missile)
        
        missile = navy_game_service.get_missiles(1)[0]
        assert not missile.is_alive

def test_missile_move_left_border():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 30, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("W", 5, 1, 1, 1, 1, 50, 2)
        navy_game_service.load_game(1)
        
        missile_service.update_position(missile)
        
        missile = navy_game_service.get_missiles(1)[0]
        assert not missile.is_alive
        
def test_missile_move_bottom_border():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 30, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("E", 20, 5, 1, 1, 1, 50, 2)
        navy_game_service.load_game(1)
        
        missile_service.update_position(missile)
        
        missile = navy_game_service.get_missiles(1)[0]
        assert not missile.is_alive
        
        
def test_missile_move_top_border():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 30, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("N", 1, 5, 1, 1, 1, 50, 2)
        navy_game_service.load_game(1)
        
        missile_service.update_position(missile)
        
        missile = navy_game_service.get_missiles(1)[0]
        assert not missile.is_alive
        
        
def test_missile_move_hit_ship():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 8, 15, "N", 1, 1, 60, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("E", 8, 13, 1, 1, 1, 30, 3)
        navy_game_service.load_game(1)
        
        missile_service.update_position(missile)
        
        missile = navy_game_service.get_missiles(1)[0]
        ship = navy_game_service.get_ships(1)[0]
        assert ship.hp == 30
        assert not missile.is_alive
        

def test_missile_move_hit_missile():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 30, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile1 = test_utils.add_test_missile("E", 8, 13, 1, 1, 1, 30, 3)
        missile2 = test_utils.add_test_missile("N", 8, 15, 1, 1, 1, 30, 3)
        navy_game_service.load_game(1)
        
        missile_service.update_position(missile1)
        
        missile1 = navy_game_service.get_missiles(1)[0]
        missile2 = navy_game_service.get_missiles(1)[1]
        assert not missile1.is_alive
        assert not missile2.is_alive


def test_missile_move_destroy_ship():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 8, 15, "N", 1, 1, 20, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("E", 8, 13, 1, 1, 1, 30, 3)
        navy_game_service.load_game(1)
        
        missile_service.update_position(missile)
        
        missile = navy_game_service.get_missiles(1)[0]
        ship = navy_game_service.get_ships(1)[0]
        assert ship.hp == -10
        assert not ship.is_alive
        assert not missile.is_alive