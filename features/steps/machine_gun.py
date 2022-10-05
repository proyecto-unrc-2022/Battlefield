import json
from platform import machine

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane, add_projectile, get_projectile, add_machine_gun
from app.models.airforce.air_force_game import AirForceGame, battlefield
from app.models.airforce.plane import Machine_gunSchema, PlaneSchema, Projectile, ProjectileSchema
from app.models.user import User

@given("an user and a plane in a valid position")
def step_impl(context):
    context.user1 = User(
        username="Maria", email="maria@gmail.com", password="12345"
    )
    db.session.add(context.user1)
    db.session.commit()

    context.plane = add_plane(
        name="Douglas A-20 Havoc", size=3, speed=5, health=10, course=1, coor_x=5, coor_y=4
    )
    assert context.plane

@when(u'create a machine gun')
def step_impl(context):
    context.machine_gun = add_machine_gun(damage_1=6, damage_2=3, damage_3=2)
    
    body = {
        "player": context.user1.id,
        "machine_gun": context.machine_gun.id,
        "x1": context.plane.coor_x,
        "y1": context.plane.coor_y,
        "course": context.plane.course,
    }
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("air_force.create_machine_gun"), data=json.dumps(body), headers=headers
    )

@then("'200' response")
def step_impl(context):
    assert context.page.status_code == 200