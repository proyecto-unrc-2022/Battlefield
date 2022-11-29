from app.models.airforce.air_force_game import AirForceGame
from app.models.airforce.commands.choose_plane import ChoosePlane
from app.models.airforce.commands.get_battlefield_status import GetBattlefieldStatus
from app.models.airforce.commands.join_game import JoinGame
from app.models.airforce.commands.launch_projectile import LaunchProjectile
from app.models.airforce.commands.move_plane import MovePlane
from app.models.airforce.plane import Plane, Projectile
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

def test_execute_list_command(app_with_plane_data):
    with app.app_context():
        game = AirForceGame()
        player_a = 0
        player_b = 1
        command = JoinGame(game, player_a)
        game.execute(command)
        command = JoinGame(game, player_b)
        game.execute(command)
        plane = Plane.query.filter_by(name="avion").first()
        print(plane)
        command = ChoosePlane(
            course=2, x=7, y=9, player=0, plane=plane, air_force_game=game
        )
        game.execute(command)
        command = ChoosePlane(
            course=4, x=13, y=4, player=1, plane=plane, air_force_game=game
        )
        game.execute(command)
        assert game.battlefield.flying_objects.__len__() == 6
        assert game.battlefield.flying_objects[0].x == 7
        assert game.battlefield.flying_objects[0].y == 9
        assert game.battlefield.flying_objects[0].course == 2
        assert game.battlefield.flying_objects[3].x == 13
        assert game.battlefield.flying_objects[3].y == 4
        assert game.battlefield.flying_objects[3].course == 4
        game.add_command(LaunchProjectile(0, game), 0)
        game.add_command(LaunchProjectile(1, game), 1)
        assert game.battlefield.flying_objects.__len__() == 8
        assert game.battlefield.flying_objects[0].x == 7
        assert game.battlefield.flying_objects[0].y == 9
        assert game.battlefield.flying_objects[0].course == 2
        assert game.battlefield.flying_objects[3].x == 13
        assert game.battlefield.flying_objects[3].y == 4
        assert game.battlefield.flying_objects[3].course == 4
        assert game.battlefield.flying_objects[6].x == 8
        assert game.battlefield.flying_objects[6].y == 9
        assert game.battlefield.flying_objects[6].course == 2
        assert game.battlefield.flying_objects[7].x == 12
        assert game.battlefield.flying_objects[7].y == 4
        assert game.battlefield.flying_objects[7].course == 4
        game.add_command(LaunchProjectile(0, game), 0)
        game.add_command(LaunchProjectile(1, game), 1)
        assert game.battlefield.flying_objects.__len__() == 10
        assert game.battlefield.flying_objects[0].x == 7
        assert game.battlefield.flying_objects[0].y == 9
        assert game.battlefield.flying_objects[0].course == 2
        assert game.battlefield.flying_objects[3].x == 13
        assert game.battlefield.flying_objects[3].y == 4
        assert game.battlefield.flying_objects[3].course == 4
        assert game.battlefield.flying_objects[6].x == 10
        assert game.battlefield.flying_objects[6].y == 9
        assert game.battlefield.flying_objects[6].course == 2
        assert game.battlefield.flying_objects[7].x == 10
        assert game.battlefield.flying_objects[7].y == 4
        assert game.battlefield.flying_objects[7].course == 4
        assert game.battlefield.flying_objects[8].x == 8
        assert game.battlefield.flying_objects[8].y == 9
        assert game.battlefield.flying_objects[8].course == 2
        assert game.battlefield.flying_objects[9].x == 12
        assert game.battlefield.flying_objects[9].y == 4
        assert game.battlefield.flying_objects[9].course == 4


def test_execute_list_command(app_with_plane_data):
    import copy
    with app.app_context():
        game = AirForceGame()
        player_a = 0
        player_b = 1
        command = JoinGame(game, player_a)
        game.execute(command)
        command = JoinGame(game, player_b)
        game.execute(command)
        plane = Plane.query.filter_by(name="avion").first()
        command = ChoosePlane(
            course=4, x=7, y=9, player=0, plane=copy.copy(plane), air_force_game=game
        )
        game.execute(command)
        command = ChoosePlane(
            course=4, x=11, y=9, player=1, plane=copy.copy(plane), air_force_game=game
        )
        game.execute(command)
        game.add_command(LaunchProjectile(0, game), 0)
        game.add_command(LaunchProjectile(1, game), 1)
        assert game.battlefield.flying_objects.__len__() == 8
        assert game.battlefield.flying_objects[0].x == 7
        assert game.battlefield.flying_objects[0].y == 9
        assert game.battlefield.flying_objects[0].course == 4
        assert game.battlefield.flying_objects[3].x == 11
        assert game.battlefield.flying_objects[3].y == 9
        assert game.battlefield.flying_objects[3].course == 4
        assert game.battlefield.flying_objects[6].x == 6
        assert game.battlefield.flying_objects[6].y == 9
        assert game.battlefield.flying_objects[6].course == 4
        assert game.battlefield.flying_objects[7].x == 10
        assert game.battlefield.flying_objects[7].y == 9
        assert game.battlefield.flying_objects[7].course == 4
        game.add_command(LaunchProjectile(0, game), 0)
        game.add_command(LaunchProjectile(1, game), 1)
        assert game.battlefield.flying_objects.__len__() == 9
        assert game.battlefield.flying_objects[0].flying_obj.health == 50
        game.add_command(LaunchProjectile(0, game), 0)
        game.add_command(LaunchProjectile(1, game), 1)
        status = game.execute(GetBattlefieldStatus(game.battlefield, game))
        print(status)
        assert status["status"] == "end" and status["Winner"] == 1

def test_launch_all_projectiles_command(app_with_plane_data):
    with app.app_context():
        game = AirForceGame()
        plane = Plane.query.filter_by(name="avion").first()
        command = ChoosePlane(
                course=4, x=7, y=9, player=0, plane=plane, air_force_game=game
            )
        game.execute(command)
        game.execute(LaunchProjectile(0, game))
        game.execute(LaunchProjectile(0, game))
        game.execute(LaunchProjectile(0, game))
        assert game.battlefield.flying_objects[0].flying_obj.cant_projectile == 0
        try:
            game.execute(LaunchProjectile(0, game))
            assert False
        except:
            assert True