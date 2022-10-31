import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane, add_projectile, get_plane
from app.models.airforce.air_force_battlefield import Battlefield
from app.models.airforce.air_force_game import AirForceGame
from app.models.airforce.plane import PlaneSchema, ProjectileSchema
from app.models.user import User

plane_schema = PlaneSchema()
proj_schema = ProjectileSchema()
air_force_game = AirForceGame()


@given("a users logged")
def step_impl(context):
    user_a = User(username="Carlitos", email="carlitos@gmail.com", password="1234")
    db.session.add(user_a)
    user_b = User(username="username", email="username@gmail.com", password="1234")
    db.session.add(user_b)
    db.session.commit()

    context.player_a = user_a.id
    context.player_b = user_b.id


@when("user_a create the game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.new_game", player=context.player_a)
    )
    print(context.response)
    context.game_id = context.response.json.get("game_id")
    assert context.response.status_code == 200


@when("user_b join in game")
def step_impl(context):
    context.response = context.client.put(
        url_for("air_force.join_in_game", player=context.player_b, id=context.game_id)
    )
    assert context.response.status_code == 200


@when("player_a add his plane")
def step_impl(context):
    players = context.client.get(url_for("air_force.get_players", id=0))
    players = players.json
    context.player_a = players.get("player_a")
    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=3,
        coor_x=5,
        coor_y=5,
    )
    context.x = 5
    context.course = 3
    context.y = 5
    projectile = add_projectile(speed=5, damage=10)
    context.plane.projectile.append(projectile)

    body = {
        "id": context.game_id,
        "player": context.player_a,
        "plane": context.plane.id,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    headers = {"Content-Type": "application/json"}
    context.page = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    print(context.page)
    assert context.page.status_code == 200


@when("player_b add his plane")
def step_impl(context):
    players = context.client.get(url_for("air_force.get_players", id=0))
    players = players.json
    context.player_b = players.get("player_b")

    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=2,
        coor_x=15,
        coor_y=5,
    )
    context.x = 15
    context.course = 2
    context.y = 5
    projectile = add_projectile(speed=5, damage=10)
    context.plane.projectile.append(projectile)

    body = {
        "id": context.game_id,
        "player": context.player_b,
        "plane": context.plane.id,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    headers = {"Content-Type": "application/json"}

    context.page = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )
    assert context.page


@then("a '200' responses")
def step_impl(context):
    raw_response = context.client.get(
        url_for("air_force.get_battlefield_status", id=context.game_id)
    ).json
    raw_expected = [
        {"course": 3, "flying_obj": 1, "player": 1, "x": 5, "y": 5},
        {"course": 2, "flying_obj": 2, "player": 2, "x": 15, "y": 5},
        {"course": 3, "flying_obj": 1, "player": "1", "x": 5, "y": 6},
        {"course": 2, "flying_obj": 2, "player": "2", "x": 16, "y": 5},
    ]
    print(raw_response)
    assert raw_expected == raw_response


@when("player_a create a projectile")
def step_impl(context):
    context.response = context.client.post(
        url_for(
            "air_force.create_projectile", id=context.game_id, player=context.player_a
        )
    )


@when("player_b create a projectile")
def step_impl(context):
    context.response = context.client.post(
        url_for(
            "air_force.create_projectile", id=context.game_id, player=context.player_b
        )
    )


# # @given("player_a and player_b in the game with their planes and projectiles available")
# # def step_impl(context):
# #     context.user1 = User(
# #         username="Carlitos", email="carlitos@gmail.com", password="1234"
# #     )
# #     db.session.add(context.user1)
# #     context.user2 = User(username="Juan", email="juan@gmail.com", password="juan1234")
# #     db.session.add(context.user2)
# #     db.session.commit()

# #     context.p1 = add_plane(
# #         name="Hawk Tempest", size=1, speed=5, health=10, course=2, coor_x=17, coor_y=7
# #     )

# #     context.p2 = add_plane(
# #         name="Mitsubishi A6M Zero",
# #         size=2,
# #         speed=5,
# #         health=20,
# #         course=4,
# #         coor_x=16,
# #         coor_y=5,
# #     )


# # @when("player_a create a projectile")
# # def step_impl(context):

# #     context.player_a_in = context.client.put(url_for("air_force.new_game", player=context.user1.id))
# #     players = context.client.get(url_for("air_force.get_players", id=0)).json
# #     context.player_a = players.get("player_a")
# #     body = {
# #         "player": context.player_a,
# #         "plane": context.p1.id,
# #         "x": 17,
# #         "y": 7,
# #         "course": 2,
# #     }
# #     headers = {"Content-Type": "application/json"}
# #     context.plane1 = context.client.post(
# #         url_for("air_force.choose_plane_and_position",id=0),
# #         data=json.dumps(body),
# #         headers=headers,
# #     )
# #     print(context.plane1.json)
# #     context.projectile = add_projectile(speed=5, damage=10)
# #     body = {
# #         "player": context.player_a,
# #     }
# #     headers = {"Content-Type": "application/json"}
# #     context.page = context.client.post(
# #         url_for("air_force.create_projectile", player=context.player_a )
# #     )

# #     assert context.page


# # @then("'200' response")
# # def step_impl(context):
# #     print(context.page.json)
# #     assert context.page.status_code == 200


# # @when("player_b create projectile")
# # def step_impl(context):

# #     context.player_b_in = context.client.put(url_for("air_force.join_in_game", player=context.user2.id, id=0))
# #     players = context.client.get(url_for("air_force.get_players", id=0)).json
# #     context.player_b = players.get("player_b")
# #     body2 = {
# #         "player": context.player_b,
# #         "plane": context.p2.id,
# #         "x": 16,
# #         "y": 5,
# #         "course": 4,
# #     }
# #     headers = {"Content-Type": "application/json"}
# #     context.plane2 = context.client.post(
# #         url_for("air_force.choose_plane_and_position", id=0),
# #         data=json.dumps(body2),
# #         headers=headers,
# #     )
# #     context.projectile = add_projectile(speed=5, damage=10)
# #     headers = {"Content-Type": "application/json"}
# #     context.response = context.client.post(
# #         url_for("air_force.create_projectile", player=context.player_b)
# #     )
# #     assert context.response


# # @then("get a '200' response")
# # def step_impl(context):
# #     assert context.response.status_code == 200


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
