import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane
from app.daos.user_dao import add_user
from app.models.airforce.air_force_game import AirForceGame
from app.models.user import User

url_for_plane_position = "air_force.choice_plane_and_position"


@given("three logged user")
def step_impl(context):
    global player_a_token, player_b_token
    add_user(username="jhon", email="jhon@email", password="1234")
    add_user(username="peter", email="Peter@email", password="pass")
    add_user(username="vladimir", email="vodka@email", password="pass")

    user_a = {"username": "jhon", "password": "1234"}
    user_b = {"username": "peter", "password": "pass"}
    user_c = {"username": "vladimir", "password": "pass"}

    headers = {"Content-Type": "application/json"}

    context.player_a_token = context.client.post(
        url_for("auth.login"), json=user_a, headers=headers
    ).json.get("token")
    context.player_b_token = context.client.post(
        url_for("auth.login"), json=user_b, headers=headers
    ).json.get("token")
    user_a = {"username": "jhon", "password": "1234"}

    context.player_c_token = context.client.post(
        url_for("auth.login"), json=user_c, headers=headers
    ).json.get("token")


@when("create new game")
def step_impl(context):
    headers = {"Authorization": f"Bearer {context.player_a_token}"}
    context.response = context.client.post(
        url_for("air_force.new_game"), headers=headers
    )
    assert context.response.status_code is 200


@then("game id are returned")
def step_impl(context):
    raw_expected = {"game_id": 0}
    raw_response = context.response.json

    response, expected = json.dumps(raw_expected, sort_keys=True), json.dumps(
        raw_response, sort_keys=True
    )
    assert response == expected


@then("players id who are in the game are returned")
def step_impl(context):
    raw_expected = {"player_a": str(context.player_a), "player_b": None}
    raw_response = context.response.json

    response, expected = json.dumps(raw_expected, sort_keys=True), json.dumps(
        raw_response, sort_keys=True
    )
    assert response == expected


@when("second user enter in the game")
def step_impl(context):
    headers = {"Authorization": f"Bearer {context.player_b_token}"}
    context.response = context.client.put(
        url_for("air_force.join_in_game", id=0), headers=headers
    )
    assert context.response.status_code is 200


@then("two users info are returned")
def step_impl(context):
    raw_expected = {
        "player_a": 1,
        "player_b": 2,
    }
    raw_response = context.response.json
    expected, response = json.dumps(raw_expected, sort_keys=True), json.dumps(
        raw_response, sort_keys=True
    )
    assert response == expected


@when("new user try enter in the game")
def step_impl(context):
    headers = {"Authorization": f"Bearer {context.player_c_token}"}
    context.response = context.client.put(
        url_for("air_force.join_in_game", id=0), headers=headers
    )


@then("status code 400 is returned")
def step_impl(context):
    assert context.response.status_code == 400


@given("player_a and plane in db")
def step_impl(context):
    context.x = 3
    context.y = 3
    context.course = 2
    add_user(username="jhon", email="jhon@email", password="1234")
    context.player = 1
    context.response = context.client.post(url_for("air_force.init_db"))
    headers = {"Content-Type": "application/json"}
    user_a = {"username": "jhon", "password": "1234"}
    context.player_a_token = context.client.post(
        url_for("auth.login"), json=user_a, headers=headers
    ).json.get("token")
    context.headers_a = {
        "Conten-Type": "application/json",
        "Authorization": f"Bearer {context.player_a_token}",
    }


@when("choose a plane and position outside of map")
def step_impl(context):
    body = {
        "id": 0,
        "plane": 1,
        "x": 21,
        "y": 11,
        "course": 2,
    }
    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        json=body,
        headers=context.headers_a,
    )
    assert context.response


@when("player_a choose a plane and his position")
def step_impl(context):
    body = {
        "id": 0,
        "plane": 1,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        json=body,
        headers=context.headers_a,
    )
    print(context.response.status_code)
    assert context.response.status_code == 200


@when("player_a choose try add new plane")
def step_impl(context):
    body = {
        "id": 0,
        "plane": 1,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        json=body,
        headers=context.headers_a,
    )


@given("player_b in the game and plane in db")
def step_impl(context):

    context.x = 13
    context.y = 6
    context.course = 4
    add_user(username="jimmy", email="jimmy@email", password="1234")
    context.player = 2
    headers = {"Content-Type": "application/json"}

    user_b = {"username": "jimmy", "password": "1234"}

    context.player_b_token = context.client.post(
        url_for("auth.login"), json=user_b, headers=headers
    ).json.get("token")

    context.headers_b = {
        "Conten-Type": "application/json",
        "Authorization": f"Bearer {context.player_b_token}",
    }
    context.client.post(url_for("air_force.init_db"))


@when("player_b choose a plane and his position")
def step_impl(context):
    body = {
        "id": 0,
        "plane": 1,
        "x": context.x,
        "y": context.y,
        "course": context.course,
    }
    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        json=body,
        headers=context.headers_b,
    )
    print(context.response.status_code)
    assert context.response.status_code == 200


@then("info of the new flying object are returned")
def step_impl(context):
    raw_response = context.response.json
    raw_expected = {
        "player": context.player,
        "flying_obj": 1,
        "x": context.x,
        "y": context.y,
        "course": context.course,
        "flying_obj_class": "Plane",
    }
    response, expected = json.dumps(raw_response, sort_keys=True), json.dumps(
        raw_expected, sort_keys=True
    )
    print(response, expected)
    assert response == expected


@then("400 response are returned")
def step_impl(context):
    assert context.response.status_code == 400


@when("choose a plane and position in player_b position")
def step_impl(context):
    body = {
        "id": 0,
        "plane": 1,
        "x": 12,
        "y": 5,
        "course": 2,
    }

    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=context.headers_a,
    )
    assert context.response


@then("Error status code are returned")
def step_impl(context):
    assert context.response.status_code == 400


@when("choose a plane and position in player_a position")
def step_impl(context):
    body = {
        "id": 0,
        "plane": 1,
        "x": 1,
        "y": 5,
        "course": 2,
    }

    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=context.headers_b,
    )
    assert context.response


@given("a battlefield with player_a's plane")
def step_impl(context):
    players = context.client.get(url_for("air_force.get_players", id=0))
    players = players.json
    context.player_a = players.get("player_a")
    context.plane = 1


@given("a battlefield with player_b's plane")
def step_impl(context):
    players = context.client.get(url_for("air_force.get_players", id=0))
    players = players.json
    context.player_b = players.get("player_b")
    context.plane = 1


@when("player_a moves his plane in th same course")
def step_impl(context):
    context.expected_x = 8
    context.expected_y = 3
    context.course = 2

    context.response = context.client.put(
        url_for(
            "air_force.fligth",
            id=0,
            course=context.course,
        ),
        headers=context.headers_a,
    )
    assert context.response.status_code is 201


@when("player_b moves his plane in th same course")
def step_impl(context):
    context.response = context.client.put(
        url_for(
            "air_force.fligth",
            id=0,
            course=4,
        ),
        headers=context.headers_b,
    )
    assert context.response.status_code is 201


@when("player_a moves his plane in new valid course")
def step_impl(context):
    context.expected_x = 8
    context.expected_y = 8
    context.course = 1
    context.response = context.client.put(
        url_for(
            "air_force.fligth",
            id=0,
            course=1,
        ),
        headers=context.headers_a,
    )
    assert context.response.status_code is 201


@when("player_b moves his plane in new valid course")
def step_impl(context):
    context.response = context.client.put(
        url_for(
            "air_force.fligth",
            id=0,
            course=3,
        ),
        headers=context.headers_b,
    )
    assert context.response.status_code is 201


@when("player_a moves his plane and colition with a limit")
def step_impl(context):
    context.expected_x = 8
    context.expected_y = 10
    context.course = 1
    context.response = context.client.put(
        url_for(
            "air_force.fligth",
            id=0,
            course=context.course,
        ),
        headers=context.headers_a,
    )


@then("201 response code are returned")
def step_impl(context):
    assert context.response.status_code == 201


@when("player_a moves his plane in invalid course")
def step_impl(context):
    context.response = context.client.put(
        url_for(
            "air_force.fligth",
            id=0,
            course=3,
        ),
        headers=context.headers_a,
    )


@then("400 response code are returned")
def step_impl(context):
    assert context.response.status_code == 400


@given("two logged users")
def step_impl(context):

    add_user(username="player1", email="vodka@email", password="pass")
    user_a = {"username": "player1", "password": "pass"}
    add_user(username="player2", email="player@email", password="pass")
    user_b = {"username": "player2", "password": "pass"}

    headers = {"Content-Type": "application/json"}
    context.player_a_token = context.client.post(
        url_for("auth.login"), json=user_a, headers=headers
    ).json.get("token")
    context.player_b_token = context.client.post(
        url_for("auth.login"), json=user_b, headers=headers
    ).json.get("token")

    context.response = context.client.post(url_for("air_force.init_db"))
    assert context.response.status_code == 200


@when("player_a create game")
def step_impl(context):
    headers = {"Authorization": f"Bearer {context.player_a_token}"}
    context.response = context.client.post(
        url_for("air_force.new_game"), headers=headers
    )
    context.game_id = context.response.json.get("game_id")
    assert context.response.status_code == 200


@when("player_b join in this game")
def step_impl(context):
    headers = {"Authorization": f"Bearer {context.player_b_token}"}
    context.response = context.client.put(
        url_for("air_force.join_in_game", id=context.game_id), headers=headers
    )


@when("player_a choose a plane")
def step_impl(context):
    body = {
        "id": context.game_id,
        "plane": 1,
        "x": 3,
        "y": 3,
        "course": 2,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {context.player_a_token}",
    }
    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )


@when("player_b choose a plane")
def step_impl(context):
    body = {
        "id": context.game_id,
        "plane": 1,
        "x": 15,
        "y": 3,
        "course": 4,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {context.player_b_token}",
    }
    context.response = context.client.put(
        url_for("air_force.choose_plane_and_position"),
        data=json.dumps(body),
        headers=headers,
    )


@when("player_a shoot a missile and player_b move his plane")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {context.player_b_token}",
    }
    context.response = context.client.put(
        url_for("air_force.fligth", id=context.game_id, course=4), headers=headers
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {context.player_a_token}",
    }
    context.response = context.client.post(
        url_for(
            "air_force.create_projectile",
            id=context.game_id,
        ),
        headers=headers,
    )
    assert context.response.status_code == 200


@when("player_a shoot second missile and player_b move his plane")
def step_impl(context):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {context.player_a_token}",
    }
    context.response = context.client.post(
        url_for("air_force.create_projectile", id=context.game_id), headers=headers
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {context.player_b_token}",
    }
    context.response = context.client.put(
        url_for("air_force.fligth", id=context.game_id, course=4), headers=headers
    )
    assert context.response.status_code == 201


@then("game status are ended")
def step_impl(context):
    context.response = context.client.get(
        url_for("air_force.get_battlefield_status", id=context.game_id)
    )

    raw_response = context.response.json
    raw_expected = {"Winner": 1, "status": "end"}

    response, expected = json.dumps(raw_response, sort_keys=True), json.dumps(
        raw_expected, sort_keys=True
    )
    assert response == expected
