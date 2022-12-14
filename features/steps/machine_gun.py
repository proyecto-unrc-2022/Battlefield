# import json
# from platform import machine

# from flask import url_for

# from app import db
# from app.daos.airforce.plane_dao import add_plane, add_machine_gun
# from app.models.airforce.plane import Machine_gunSchema, PlaneSchema, Projectile, ProjectileSchema
# from app.models.user import User

# @given("an user and a plane in a valid position")
# def step_impl(context):
#     context.user1 = User(
#     username="Maria", email="maria@gmail.com", password="12345"
#     )
#     db.session.add(context.user1)
#     db.session.commit()
#     context.response = context.client.post(url_for("air_force.init_db"))

# @when(u'create a machine gun')
# def step_impl(context):
#     context.machine_gun = add_machine_gun(damage_1=6, damage_2=3, damage_3=2)

#     body = {
#     "player": context.user1.id,
#     "machine_gun": context.machine_gun.id,
#     "damage_1": context.machine_gun.damage_1,
#     "damage_2": context.machine_gun.damage_2,
#     "damage_3": context.machine_gun.damage_3,
#     "x1": context.plane.coor_x,
#     "y1": context.plane.coor_y,
#     "course": context.plane.course,
#     }
#     headers = {"Content-Type": "application/json"}
#     context.page = context.client.post(
#     url_for("air_force.create_machine_gun"), data=json.dumps(body), headers=headers
#     )

# @then("'200' resp.")
# def step_impl(context):
#     assert context.page.status_code == 200
