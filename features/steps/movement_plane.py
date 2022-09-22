import json

from flask import url_for

from app.daos.airforce.plane_dao import add_plane


@given("A plane on the map")
def step_impl(context):
    context.plane = add_plane(
        name="Douglas A-20 Havoc",
        size=3,
        speed=2,
        health=40,
        course="east",
        coor_x=7,
        coor_y=4,
    )
    return context.plane


@when("I make the rotation")
def step_impl(context):
    plane_id = context.plane.id
    body = {"id": plane_id, "course": "south"}
    headers = {"Content-Type": "application/json"}
    context.page = context.client.put(
        url_for("air_force.update_course"), data=json.dumps(body), headers=headers
    )
    assert context.page


@then("I should obtain a '201' response")
def step_impl(context):
    print(context.page.status_code)
    assert context.page.status_code is 201
