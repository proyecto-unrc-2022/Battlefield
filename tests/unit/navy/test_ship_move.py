from battlefield import app
from features.steps.navy.test_utils import test_utils
from app.navy.services.ship_service import ship_service
from app.navy.services.navy_game_service import navy_game_service


def test_ship_move_without_collision():
    with app.app_context():
        #Arrange
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 60, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        navy_game_service.load_game(1)
        
        #Act
        ship_service.update_position(ship, 3)
        
        #Assert
        ship = navy_game_service.get_ships(1)[0]
        assert ship.pos_x == 2 and ship.pos_y == 5
        
        
def test_ship_move_missile_collision():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 60, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("E", 4, 5, 1, 1, 1, 30, 2)
        navy_game_service.load_game(1)
        
        ship_service.update_position(ship, 3)
        
        ship = navy_game_service.get_ships(1)[0]
        missile = navy_game_service.get_missiles(1)[0]
        assert ship.pos_x == 2 and ship.pos_y == 5
        assert ship.hp == 30
        assert not missile.is_alive
        
def test_ship_move_destruction_missile():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 60, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("E", 4, 5, 1, 1, 1, 70, 2)
        navy_game_service.load_game(1)
        
        ship_service.update_position(ship, 3)
        
        missile = navy_game_service.get_missiles(1)[0]
        ship = navy_game_service.get_ships(1)[0]
        assert not missile.is_alive
        assert ship.pos_x == 4 and ship.pos_y == 5
        assert ship.hp == -10
        assert not ship.is_alive
        
def test_ship_move_destruction_two_missiles():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 60, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile1 = test_utils.add_test_missile("E", 4, 5, 1, 1, 1, 40, 2)
        missile2 = test_utils.add_test_missile("E", 3, 5, 1, 1, 1, 40, 2)
        navy_game_service.load_game(1)
        
        ship_service.update_position(ship, 3)
        
        missile1 = navy_game_service.get_missiles(1)[0]
        missile2 = navy_game_service.get_missiles(1)[1]
        ship = navy_game_service.get_ships(1)[0]
        assert not missile1.is_alive
        assert not missile2.is_alive
        assert ship.pos_x == 3 and ship.pos_y == 5
        assert ship.hp == -20
        assert not ship.is_alive
        
def test_ship_move_ship_collision():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship1 = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 70, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 4, 5, "W", 2, 1, 100, 3, 3, 5, 1)
        navy_game_service.load_game(1)
        
        ship_service.update_position(ship1, 3)
        ship1 =  navy_game_service.get_ships(1)[0]
        ship2 =  navy_game_service.get_ships(1)[1]
        game = navy_game_service.get_by_id(1)
        assert ship1.pos_x == 4 and ship1.pos_y == 5
        assert ship1.hp == -30
        assert not ship1.is_alive
        assert ship2.hp == 30
        assert game.winner == 2