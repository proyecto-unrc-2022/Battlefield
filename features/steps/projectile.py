import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane, add_projectile, get_projectile
from app.models.airforce.air_force_game import AirForceGame, battlefield
from app.models.airforce.plane import PlaneSchema, Projectile, ProjectileSchema
from app.models.user import User

plane_schema = PlaneSchema()
proj_scehma = ProjectileSchema()


@given("a plane in a valid position")
def step_impl(context):
    context.user1 = User(
        username="Carlitos", email="carlitos@gmail.com", password="1234"
    )
    db.session.add(context.user1)
    db.session.commit()

    context.plane = add_plane(
        name="Hawk Tempest", size=1, speed=5, health=10, course=2, coor_x=5, coor_y=7
    )
    assert context.plane


@when("create a projectile")
def step_impl(context):
    context.projectile = add_projectile(speed=5, damage=10)
    body = {
        "player": context.user1.id,
        "projectile": context.projectile.id,
        "x": context.plane.coor_x,
        "y": context.plane.coor_y,
        "course": context.plane.course,
    }
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("air_force.create_projectile"), data=json.dumps(body), headers=headers
    )

    assert context.page


@then("'200' response")
def step_impl(context):
    assert context.page.status_code == 200


# ----------------------------------------------------------------------------------------------------------------


@given("a projectile in some place of the map")
def step_impl(context):

    context.user1 = User(username="Carlos", email="carlito@gmail.com", password="1234")
    db.session.add(context.user1)
    db.session.commit()

    context.projectile = add_projectile(speed=5, damage=10)
    context.get_proj = get_projectile(projectile_id=context.projectile.id)

    context.object = battlefield.add_new_projectile(
        player=context.user1.id,
        flying_object=proj_scehma.dump(context.get_proj),
        x=6,
        y=5,
        course=1,
    )


@when("a new shift starts")
def step_impl(context):

    body = {"object": context.object}
    headers = {"Content-Type": "application/json"}

    context.response = context.client.put(
        url_for("air_force.update_location_projectile"),
        data=json.dumps(body),
        headers=headers,
    )


@then("the projectile moved the speed corresponding")
def step_impl(context):
    assert context.response.status_code == 200
