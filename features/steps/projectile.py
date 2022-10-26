# import json

# from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane, add_projectile
from app.models.airforce.air_force_battlefield import Battlefield
from app.models.airforce.air_force_game import AirForceGame
from app.models.airforce.plane import PlaneSchema, ProjectileSchema
from app.models.user import User

plane_schema = PlaneSchema()
proj_schema = ProjectileSchema()
air_force_game = AirForceGame()


@given("player_a and player_b in the game with their planes and projectiles available")
def step_impl(context):
    context.user1 = User(
        username="Carlitos", email="carlitos@gmail.com", password="1234"
    )
    db.session.add(context.user1)
    context.user2 = User(username="Juan", email="juan@gmail.com", password="juan1234")
    db.session.add(context.user2)
    db.session.commit()

    context.p1 = add_plane(
        name="Hawk Tempest", size=1, speed=5, health=10, course=2, coor_x=17, coor_y=7
    )

    context.p2 = add_plane(
        name="Mitsubishi A6M Zero",
        size=2,
        speed=5,
        health=20,
        course=4,
        coor_x=16,
        coor_y=5,
    )


@when("player_a create a projectile")
def step_impl(context):

    context.player_a = air_force_game.join_game(new_player=context.user1.id).get(
        "player_a"
    )

    body = {
        "player": context.player_a,
        "plane": context.p1.id,
        "x": 17,
        "y": 7,
        "course": 2,
    }
    headers = {"Content-Type": "application/json"}
    context.plane1 = context.client.post(
        url_for("air_force.choice_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    print(context.plane1.json)
    context.projectile = add_projectile(speed=5, damage=10)
    body = {
        "player": context.player_a,
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


@when("player_b create projectile")
def step_impl(context):

    context.player_b = air_force_game.join_game(new_player=context.user2.id).get(
        "player_b"
    )

    body2 = {
        "player": context.player_b,
        "plane": context.p2.id,
        "x": 16,
        "y": 5,
        "course": 4,
    }
    headers = {"Content-Type": "application/json"}
    context.plane2 = context.client.post(
        url_for("air_force.choice_plane_and_position"),
        data=json.dumps(body2),
        headers=headers,
    )
    context.projectile = add_projectile(speed=5, damage=10)
    body = {
        "player": context.player_b,
    }
    headers = {"Content-Type": "application/json"}
    context.response = context.client.post(
        url_for("air_force.create_projectile"), data=json.dumps(body), headers=headers
    )
    assert context.response


@then("get a '200' response")
def step_impl(context):
    assert context.response.status_code == 200


# ----------------------------------------------------------------------------------------------------------------


# @given("projectile of player_a in the battlefield")
# def step_impl(context):
#     context.projectile = add_projectile(speed=5, damage=10)
#     # context.flying_o = AirForceGame.battlefield.add_new_projectile(
#     #     player=1,
#     #     obj=context.projectile,
#     #     x=10,
#     #     y=7,
#     #     course=2,
#     # )


# @when("a new turn starts and the projectiles of player_a have to be updated")
# def step_impl(context):
#     context.response = context.client.put(
#         url_for(
#             "air_force.move_projectile",
#             player_projectile=1,
#             plane_id=1,
#         )
#     )


# @then("the projectiles of player_a moves the speed corresponding")
# def step_impl(context):
#     print(context.response.json)
#     assert context.response.status_code == 200


# ------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------


# @given("a projectile of player_b in the")
# def step_impl(context):
#     context.projectile = add_projectile(speed=5, damage=10)
#     # context.flying_o = AirForceGame.battlefield.add_new_projectile(
#     #     player=2,
#     #     plane=context.plane2,
#     #     projectile=context.projectile,
#     # )


# @when("a new turn starts and the projectiles of player_b have to be updated")
# def step_impl(context):
#     context.response = context.client.put(
#         url_for(
#             "air_force.move_projectile",
#             player_projectile=2,
#             plane_id=2,
#         )
#     )


# @then("the projectile of player_b moves the speed corresponding")
# def step_impl(context):
#     print(context.response.json)
#     assert context.response.status_code != 200


# # ------------------------------------------------------------------------------------------------------------


# @given("two or more projectile in the battlefield")
# def step_impl(context):
#     context.proj1 = add_projectile(speed=5, damage=10)
#     # context.projectile1 = AirForceGame.battlefield.add_new_projectile(
#     #     player=1,
#     #     obj=context.proj1,
#     #     x=8,
#     #     y=7,
#     #     course=2,
#     # )
#     context.proj2 = add_projectile(speed=5, damage=20)
#     # context.projectile2 = AirForceGame.battlefield.add_new_projectile(
#     #     player=2,
#     #     obj=context.proj2,
#     #     x=12,
#     #     y=7,
#     #     course=4,
#     # )


# @when("a collision occurs")
# def step_impl(context):
#     context.response = context.client.put(
#         url_for("air_force.move_projectile", player_projectile=2, course=4)
#     )


# @then("a '200' response")
# def step_impl(context):
#     assert context.response.status_code == 200
