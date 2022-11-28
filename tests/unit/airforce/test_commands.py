from app.models.airforce.air_force_game import AirForceGame
from app.models.airforce.commands.choose_plane import ChoosePlane
from app.models.airforce.commands.join_game import JoinGame
from app.models.airforce.plane import Plane
from battlefield import app


def test_user_join_game():
    with app.app_context():
        game = AirForceGame()
        player_a = 0
        player_b = 1
        command = JoinGame(game, player_a)
        game.execute(command)
        command = JoinGame(game, player_b)
        game.execute(command)
        assert game.player_b == 1
        assert game.player_a == 0


def test_user_cant_join_game():
    with app.app_context():
        game = AirForceGame()
        player_a = 0
        command = JoinGame(game, player_a)
        game.execute(command)
        command = JoinGame(game, player_a)
        try:
            game.execute(command)
            assert False
        except Exception as e:
            assert e.args[0] == "Players must be differents"
            assert True


def test_choose_plane_command():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=3, speed=2, health=100, cant_projectile=2
        )
        game = AirForceGame()
        player_a = 0
        player_b = 1
        command = JoinGame(game, player_a)
        game.execute(command)
        command = JoinGame(game, player_b)
        game.execute(command)
        command = ChoosePlane(
            course=1, x=7, y=9, player=0, plane=plane, air_force_game=game
        )
        game.execute(command)
        assert game.battlefield.flying_objects.__len__() == 3
        assert game.battlefield.flying_objects[0].x == 7
        assert game.battlefield.flying_objects[0].y == 9
        assert game.battlefield.flying_objects[0].course == 1
        assert game.battlefield.flying_objects[1].x == 7
        assert game.battlefield.flying_objects[1].y == 8
        assert game.battlefield.flying_objects[1].course == 1
        assert game.battlefield.flying_objects[2].x == 7
        assert game.battlefield.flying_objects[2].y == 7
        assert game.battlefield.flying_objects[2].course == 1


def test_choose_plane_in_border():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=3, speed=2, health=100, cant_projectile=2
        )
        game = AirForceGame()
        player_a = 0
        player_b = 1
        command = JoinGame(game, player_a)
        game.execute(command)
        command = JoinGame(game, player_b)
        game.execute(command)
        command = ChoosePlane(
            course=3, x=7, y=9, player=0, plane=plane, air_force_game=game
        )
        game.execute(command)
        assert game.battlefield.flying_objects.__len__() == 3
        assert game.battlefield.flying_objects[0].x == 7
        assert game.battlefield.flying_objects[0].y == 9
        assert game.battlefield.flying_objects[0].course == 3
        assert game.battlefield.flying_objects[1].x == 7
        assert game.battlefield.flying_objects[1].y == 10
        assert game.battlefield.flying_objects[1].course == 3
        assert game.battlefield.flying_objects[2].x == 7
        assert game.battlefield.flying_objects[2].y == 11
        assert game.battlefield.flying_objects[2].course == 3
