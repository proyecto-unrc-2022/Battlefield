from app.models.airforce.air_force_flying_object import FlyingObject
from app.models.airforce.airforce_db_utils import init_db_planes
from battlefield import app
from app.models.airforce.plane import Plane

def test_check_invalid_course():
    with app.app_context():
        init_db_planes()
        plane = Plane.query.filter_by(id=0).first()
        fly_obj = FlyingObject(player=1, flying_obj=plane, x=2, y=2, course=1)
        assert fly_obj.check_invalid_course(3)

def test_check_valid_course():
    with app.app_context():
        init_db_planes()
        plane = Plane.query.filter_by(id=0).first()
        fly_obj = FlyingObject(player=1, flying_obj=plane, x=2, y=2, course=1)
        assert fly_obj.check_invalid_course(4) == False

def test_update_postion_invalid_position():
    with app.app_context():
        init_db_planes()
        plane = Plane.query.filter_by(id=0).first()
        fly_obj = FlyingObject(player=1, flying_obj=plane, x=2, y=2, course=1)
        try:
            fly_obj.update_position(3,20,10)
            assert False
        except:
            assert True

def test_update_postion_north():
    with app.app_context():
        plane = Plane(id=0, name= "avion", size= 1, speed=2, health=100, cant_projectile=2)
        fly_obj = FlyingObject(player=1, flying_obj=plane, x=2, y=2, course=1)
        old_position = fly_obj.y
        fly_obj.update_position(1,20,10)
        assert fly_obj.y == old_position + fly_obj.flying_obj.speed

def test_update_postion_south():
    with app.app_context():
        plane = Plane(id=0, name= "avion", size= 1, speed=2, health=100, cant_projectile=2)
        print(plane)
        fly_obj = FlyingObject(player=1, flying_obj=plane, x=2, y=6, course=3)
        old_position = fly_obj.y
        fly_obj.update_position(3,20,10)
        assert fly_obj.y == old_position - fly_obj.flying_obj.speed 

def test_update_postion_east():
    with app.app_context():
        plane = Plane(id=0, name= "avion", size= 1, speed=2, health=100, cant_projectile=2)
        print(plane)
        fly_obj = FlyingObject(player=1, flying_obj=plane, x=5, y=2, course=1)
        old_position = fly_obj.x
        fly_obj.update_position(2,20,10)
        assert fly_obj.x == old_position + fly_obj.flying_obj.speed

def test_update_postion_weast():
    with app.app_context():
        plane = Plane(id=0, name= "avion", size= 1, speed=2, health=100, cant_projectile=2)
        print(plane)
        fly_obj = FlyingObject(player=1, flying_obj=plane, x=5, y=2, course=1)
        old_position = fly_obj.x
        fly_obj.update_position(4,20,10)
        assert fly_obj.x == old_position - fly_obj.flying_obj.speed