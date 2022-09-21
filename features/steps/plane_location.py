import json

from flask import url_for

from app.daos.airforce.plane_dao import add_game, add_plane


@given("a map with no planes in it")
def step_impl(context):
    context.game = add_game(player_a_id=1, player_b_id=2)


@when("i place a plane")
def step_impl(context):
    body = {
        "name": "Mitsubishi A6M Zero",
        "size": 2,
        "speed": 3,
        "health": 20,
        "direct_of_plane": "north",
        "coor_x": 10,
        "coor_y": 10,
    }
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("air_force.put_plane"), data=json.dumps(body), headers=headers
    )
    assert context.page


@then("i should get a '200' response")
def step_impl(context):
    assert context.page.status_code is 200


@then("the plane is in a correctly position")
def step_impl(context):
    pass
