import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane, add_projectile, get_projectile
from app.models.airforce.air_force_game import AirForceGame, battlefield
from app.models.airforce.plane import PlaneSchema, Projectile, ProjectileSchema
from app.models.user import User

plane_schema = PlaneSchema()
proj_schema = ProjectileSchema()


@given("a player who has a plane and a launched projectile in the battlefield")
def step_impl(context):
    context.user1 = User(
        username="Carlitos", email="carlitos@gmail.com", password="1234"
    )
    db.session.add(context.user1)
    db.session.commit()

    context.plane = add_plane(
        name="Hawk Tempest", size=1, speed=5, health=10, course=2, coor_x=17, coor_y=7
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
    print(context.page.json)
    assert context.page.status_code == 200


# ----------------------------------------------------------------------------------------------------------------


@given("a new projectile created and new shift begin")
def step_impl(context):
    context.projectile = add_projectile(speed=5, damage=10)
    context.flying_o = AirForceGame.battlefield.add_new_projectile(
        player=1,
        obj=context.projectile,
        x=10,
        y=7,
        course=2,
    )


@when("a new shift starts")
def step_impl(context):
    context.response = context.client.put(
        url_for(
            "air_force.move_projectile",
            player_projectile=1,
            course=2,
        )
    )


@then("the projectiles move the speed corresponding")
def step_impl(context):
    assert context.response.status_code == 200
