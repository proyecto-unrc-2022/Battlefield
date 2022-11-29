from app.models.airforce.air_force_battlefield import Battlefield
from app.models.airforce.air_force_game import AirForceGame
from app.models.airforce.airforce_filters import get_player_plane
from app.models.airforce.plane import Plane, Projectile
from battlefield import app


def test_add_plane():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 2)
        assert battlefield.flying_objects.__len__() == 1
        assert battlefield.flying_objects[0].flying_obj == plane


def test_add_plane_another_plane():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 2)
        battlefield.add_new_flying_object(0, plane, 17, 5, 4)
        assert battlefield.flying_objects.__len__() == 2
        assert battlefield.flying_objects[0].flying_obj == plane
        assert battlefield.flying_objects[1].flying_obj == plane


def test_add_plane_outside_map():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        try:
            battlefield.add_new_flying_object(0, plane, 25, 15, 2)
            assert False
        except:
            assert True


def test_move_north():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 1)
        battlefield.move(get_player_plane(battlefield, 0)[0], 1)
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 7
        assert battlefield.flying_objects[0].course == 1


def test_move_south():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 2)
        battlefield.move(get_player_plane(battlefield, 0)[0], 3)
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 3
        assert battlefield.flying_objects[0].course == 3


def test_move_east():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 1)
        battlefield.move(get_player_plane(battlefield, 0)[0], 2)
        assert battlefield.flying_objects[0].x == 7
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2


def test_move_west():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 3)
        battlefield.move(get_player_plane(battlefield, 0)[0], 4)
        assert battlefield.flying_objects[0].x == 3
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 4


def test_rotate_north():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=3, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 2)
        battlefield.add_new_flying_object(0, plane, 5 - 1, 5, 2)
        battlefield.add_new_flying_object(0, plane, 5 - 2, 5, 2)
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2
        assert battlefield.flying_objects[1].x == 4
        assert battlefield.flying_objects[1].y == 5
        assert battlefield.flying_objects[1].course == 2
        assert battlefield.flying_objects[2].x == 3
        assert battlefield.flying_objects[2].y == 5
        assert battlefield.flying_objects[2].course == 2
        battlefield.move(get_player_plane(battlefield, 0)[0], 1)
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 7
        assert battlefield.flying_objects[0].course == 1
        assert battlefield.flying_objects[1].x == 5
        assert battlefield.flying_objects[1].y == 6
        assert battlefield.flying_objects[1].course == 1
        assert battlefield.flying_objects[2].x == 5
        assert battlefield.flying_objects[2].y == 5
        assert battlefield.flying_objects[2].course == 1


def test_rotate_east():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=3, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 5, 3)
        battlefield.add_new_flying_object(0, plane, 5, 5 + 1, 3)
        battlefield.add_new_flying_object(0, plane, 5, 5 + 2, 3)
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 3
        assert battlefield.flying_objects[1].x == 5
        assert battlefield.flying_objects[1].y == 6
        assert battlefield.flying_objects[1].course == 3
        assert battlefield.flying_objects[2].x == 5
        assert battlefield.flying_objects[2].y == 7
        assert battlefield.flying_objects[2].course == 3
        battlefield.move(get_player_plane(battlefield, 0)[0], 2)
        assert battlefield.flying_objects[0].x == 7
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2
        assert battlefield.flying_objects[1].x == 6
        assert battlefield.flying_objects[1].y == 5
        assert battlefield.flying_objects[1].course == 2
        assert battlefield.flying_objects[2].x == 5
        assert battlefield.flying_objects[2].y == 5
        assert battlefield.flying_objects[2].course == 2


def test_move_plane_colision_with_x_limit():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 19, 5, 2)
        battlefield.move(get_player_plane(battlefield, 0)[0], 2)
        assert battlefield.flying_objects[0].x == 20
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2


def test_move_plane_colision_with_y_limit():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 19, 1, 3)
        battlefield.move(get_player_plane(battlefield, 0)[0], 3)
        assert battlefield.flying_objects[0].x == 19
        assert battlefield.flying_objects[0].y == 0
        assert battlefield.flying_objects[0].course == 3


def test_move_two_planes():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 15, 5, 2)
        battlefield.add_new_flying_object(1, plane, 15, 7, 4)
        battlefield.move(get_player_plane(battlefield, 0)[0], 2)
        battlefield.move(get_player_plane(battlefield, 1)[0], 4)
        assert battlefield.flying_objects[0].x == 17
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2
        assert battlefield.flying_objects[1].x == 13
        assert battlefield.flying_objects[1].y == 7
        assert battlefield.flying_objects[1].course == 4


def test_move_plane_colision_from_east():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        plane_2 = Plane(
            id=1, name="avion", size=1, speed=2, health=70, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 6, 5, 2)
        battlefield.add_new_flying_object(1, plane_2, 7, 5, 1)
        battlefield.move(get_player_plane(battlefield, 0)[0], 2)
        assert battlefield.flying_objects[0].x == 8
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2
        assert battlefield.flying_objects[0].flying_obj.health == 30
        assert battlefield.flying_objects.__len__() == 1


def test_move_plane_colision_from_west():
    with app.app_context():
        plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
        plane_2 = Plane(
            id=1, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 6, 5, 2)
        battlefield.add_new_flying_object(1, plane_2, 7, 5, 4)
        battlefield.move(get_player_plane(battlefield, 1)[0], 4)
        assert battlefield.flying_objects.__len__() == 1
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 4
        assert battlefield.flying_objects[0].flying_obj.health == 30


def test_move_plane_colision_from_north():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        plane_2 = Plane(
            id=1, name="avion", size=1, speed=2, health=70, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 6, 1)
        battlefield.add_new_flying_object(1, plane_2, 5, 7, 3)
        battlefield.move(get_player_plane(battlefield, 0)[0], 1)
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 8
        assert battlefield.flying_objects[0].course == 1
        assert battlefield.flying_objects[0].flying_obj.health == 30
        assert battlefield.flying_objects.__len__() == 1


def test_move_plane_colision_from_south():
    with app.app_context():
        plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
        plane_2 = Plane(
            id=1, name="avion", size=1, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 5, 6, 1)
        battlefield.add_new_flying_object(1, plane_2, 5, 7, 3)
        battlefield.move(get_player_plane(battlefield, 1)[0], 3)
        assert battlefield.flying_objects.__len__() == 1
        assert battlefield.flying_objects[0].x == 5
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 3
        assert battlefield.flying_objects[0].flying_obj.health == 30


def test_move_projectile_colision():
    with app.app_context():
        plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
        projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, projectile, 5, 6, 1)
        battlefield.add_new_flying_object(1, projectile, 5, 7, 3)
        battlefield.move(battlefield.flying_objects[0], 1)
        assert battlefield.flying_objects.__len__() == 0


def test_move_projectile_colision_plane():
    plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    battlefield = Battlefield()
    battlefield.add_new_flying_object(0, projectile, 5, 6, 1)
    battlefield.add_new_flying_object(1, plane, 5, 7, 3)
    battlefield.move(battlefield.flying_objects[0], 1)
    assert battlefield.flying_objects.__len__() == 1
    assert battlefield.flying_objects[0].x == 5
    assert battlefield.flying_objects[0].y == 7
    assert battlefield.flying_objects[0].course == 3
    assert battlefield.flying_objects[0].flying_obj.health == 20


def test_move_projectile_colision_y_max_limit():
    plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    battlefield = Battlefield()
    battlefield.add_new_flying_object(0, projectile, 5, 9, 1)
    battlefield.add_new_flying_object(0, projectile, 15, 8, 1)
    battlefield.move_projectile(0)
    assert battlefield.flying_objects.__len__() == 1
    assert battlefield.flying_objects[0].y == 10
    assert battlefield.flying_objects[0].x == 15
    assert battlefield.flying_objects[0].course == 1


def test_move_projectile_colision_y_min_limit():
    plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    battlefield = Battlefield()
    battlefield.add_new_flying_object(0, projectile, 5, 1, 3)
    battlefield.add_new_flying_object(0, projectile, 15, 2, 3)
    battlefield.move_projectile(0)
    assert battlefield.flying_objects.__len__() == 1
    assert battlefield.flying_objects[0].y == 0
    assert battlefield.flying_objects[0].x == 15
    assert battlefield.flying_objects[0].course == 3


def test_move_projectile_colision_x_max_limit():
    plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    battlefield = Battlefield()
    battlefield.add_new_flying_object(0, projectile, 19, 4, 2)
    battlefield.add_new_flying_object(0, projectile, 18, 8, 2)
    battlefield.move_projectile(0)
    assert battlefield.flying_objects.__len__() == 1
    assert battlefield.flying_objects[0].y == 8
    assert battlefield.flying_objects[0].x == 20
    assert battlefield.flying_objects[0].course == 2


def test_move_projectile_colision_x_min_limit():
    plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    battlefield = Battlefield()
    battlefield.add_new_flying_object(0, projectile, 1, 7, 4)
    battlefield.add_new_flying_object(0, projectile, 2, 6, 4)
    battlefield.move_projectile(0)
    assert battlefield.flying_objects.__len__() == 1
    assert battlefield.flying_objects[0].y == 6
    assert battlefield.flying_objects[0].x == 0
    assert battlefield.flying_objects[0].course == 4


def test_projectile_destroy_plane():
    plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    battlefield = Battlefield()
    battlefield.add_new_flying_object(0, projectile, 5, 6, 1)
    battlefield.add_new_flying_object(0, projectile, 5, 4, 1)
    battlefield.add_new_flying_object(1, plane, 5, 7, 3)
    battlefield.move(battlefield.flying_objects[0], 1)
    battlefield.move(battlefield.flying_objects[0], 1)
    battlefield.move(battlefield.flying_objects[0], 1)
    assert battlefield.flying_objects.__len__() == 0


def test_projectiles_one_player():
    plane = Plane(id=0, name="avion", size=1, speed=2, health=70, cant_projectile=2)
    projectile = Projectile(id=0, speed=2, damage=50, plane_id=plane.id)
    battlefield = Battlefield()
    battlefield.add_new_flying_object(0, projectile, 10, 6, 1)
    battlefield.add_new_flying_object(0, projectile, 16, 5, 3)
    battlefield.add_new_flying_object(0, projectile, 5, 2, 2)
    battlefield.add_new_flying_object(0, projectile, 16, 9, 4)
    battlefield.move_projectile(0)
    assert battlefield.flying_objects.__len__() == 4
    assert battlefield.flying_objects[0].x == 10
    assert battlefield.flying_objects[0].y == 8
    assert battlefield.flying_objects[0].course == 1
    assert battlefield.flying_objects[1].x == 16
    assert battlefield.flying_objects[1].y == 3
    assert battlefield.flying_objects[1].course == 3
    assert battlefield.flying_objects[2].x == 7
    assert battlefield.flying_objects[2].y == 2
    assert battlefield.flying_objects[2].course == 2
    assert battlefield.flying_objects[3].x == 14
    assert battlefield.flying_objects[3].y == 9
    assert battlefield.flying_objects[3].course == 4


def test_hit_big_plane():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=3, speed=2, health=100, cant_projectile=2
        )
        projectile = Projectile(id=0, speed=5, damage=50, plane_id=plane.id)
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 7, 5, 2)
        battlefield.add_new_flying_object(0, plane, 6, 5, 2)
        battlefield.add_new_flying_object(0, plane, 5, 5, 2)
        battlefield.add_new_flying_object(1, projectile, 9, 5, 4)
        battlefield.move_projectile(1)
        assert battlefield.flying_objects.__len__() == 3
        assert battlefield.flying_objects[0].flying_obj == plane
        assert battlefield.flying_objects[1].flying_obj == plane
        assert battlefield.flying_objects[2].flying_obj == plane
        assert battlefield.flying_objects[0].x == 7
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2
        assert battlefield.flying_objects[0].flying_obj.health == 50
        assert battlefield.flying_objects[1].x == 6
        assert battlefield.flying_objects[1].y == 5
        assert battlefield.flying_objects[1].course == 2
        assert battlefield.flying_objects[1].flying_obj.health == 50
        assert battlefield.flying_objects[2].x == 5
        assert battlefield.flying_objects[2].y == 5
        assert battlefield.flying_objects[2].course == 2
        assert battlefield.flying_objects[2].flying_obj.health == 50


def test_destroy_big_plane():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=3, speed=2, health=100, cant_projectile=2
        )
        projectile = Projectile(id=0, speed=5, damage=50, plane_id=plane.id)
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 7, 5, 2)
        battlefield.add_new_flying_object(0, plane, 6, 5, 2)
        battlefield.add_new_flying_object(0, plane, 5, 5, 2)
        battlefield.add_new_flying_object(1, projectile, 9, 5, 4)
        battlefield.add_new_flying_object(1, projectile, 6, 7, 3)
        battlefield.move_projectile(1)
        assert battlefield.flying_objects.__len__() == 0


def test_big_plane_move():
    with app.app_context():
        plane = Plane(
            id=0, name="avion", size=3, speed=2, health=100, cant_projectile=2
        )
        battlefield = Battlefield()
        battlefield.add_new_flying_object(0, plane, 7, 5, 2)
        battlefield.add_new_flying_object(0, plane, 6, 5, 2)
        battlefield.add_new_flying_object(0, plane, 5, 5, 2)
        battlefield.move(battlefield.flying_objects[0], 2)
        assert battlefield.flying_objects.__len__() == 3
        assert battlefield.flying_objects[0].x == 9
        assert battlefield.flying_objects[0].y == 5
        assert battlefield.flying_objects[0].course == 2
        assert battlefield.flying_objects[1].x == 8
        assert battlefield.flying_objects[1].y == 5
        assert battlefield.flying_objects[1].course == 2
        assert battlefield.flying_objects[2].x == 7
        assert battlefield.flying_objects[2].y == 5
        assert battlefield.flying_objects[2].course == 2
