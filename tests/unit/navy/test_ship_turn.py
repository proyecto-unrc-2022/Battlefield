from battlefield import app
from features.steps.navy.test_utils import test_utils
from app.navy.services.ship_service import ship_service
from app.navy.services.navy_game_service import navy_game_service


def test_ship_turn_without_collision():
    with app.app_context():
        #Arrange
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 4, "W", 1, 1, 60, 3, 3, 5, 1)
        navy_game_service.load_game(1)
        
        #Act
        ship_service.turn(ship, "E")
        
        #Assert
        ship = navy_game_service.get_ships(1)[0]
        assert ship.course == "E"
        
    
def test_ship_turn_missile_collision():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 60, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("W", 5, 7, 1, 1, 1, 30, 1)
        navy_game_service.load_game(1)
        
        ship_service.turn(ship, "W")

        missile = navy_game_service.get_missiles(1)[0]
        ship = navy_game_service.get_ships(1)[0]
        assert ship.course == "W"
        assert ship.hp == 30
        assert not missile.is_alive
        
        
def test_ship_turn_destruction_missile():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 30, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile = test_utils.add_test_missile("W", 5, 7, 1, 1, 1, 40, 1)
        navy_game_service.load_game(1)
        
        ship_service.turn(ship, "W")

        missile = navy_game_service.get_missiles(1)[0]
        ship = navy_game_service.get_ships(1)[0]
        assert not missile.is_alive
        assert ship.course == "W"
        assert ship.hp == -10
        assert not ship.is_alive
    

def test_ship_turn_destruction_two_missiles():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship = test_utils.add_test_ship("Destroyer", 5, 5, "N",1, 1, 70, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 15, "N", 2, 1, 30, 3, 3, 5, 1)
        missile1 = test_utils.add_test_missile("W", 5, 6, 1, 1, 1, 40, 1)
        missile2 = test_utils.add_test_missile("W", 5, 7, 1, 1, 1, 40, 1)
        navy_game_service.load_game(1)
        
        ship_service.turn(ship, "W")

        missile1 =  navy_game_service.get_missiles(1)[0]
        missile2 =  navy_game_service.get_missiles(1)[1]
        ship =  navy_game_service.get_ships(1)[0]
        assert not missile1.is_alive
        assert not missile2.is_alive
        assert ship.course == "W"
        assert ship.hp == -10
        assert not ship.is_alive
        
         
def test_ship_turn_ship_collision():
    with app.app_context():
        test_utils.arrange_navy_game()
        ship1 = test_utils.add_test_ship("Destroyer", 5, 5, "N", 1, 1, 70, 3, 3, 5, 1)
        ship2 = test_utils.add_test_ship("Destroyer", 5, 6, "N", 2, 1, 100, 3, 3, 5, 1)
        navy_game_service.load_game(1)
        
        ship_service.turn(ship1, "W")
        
        ship1 =  navy_game_service.get_ships(1)[0]
        ship2 =  navy_game_service.get_ships(1)[1]
        game = navy_game_service.get_by_id(1)
        assert ship1.course == "W"
        assert ship1.hp == -30
        assert not ship1.is_alive
        assert ship2.hp == 30
        assert game.winner == 2
        