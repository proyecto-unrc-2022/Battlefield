import dbm
import json

from flask import url_for

from app import db
from app.daos.airforce.plane_dao import add_plane
from app.models.airforce.plane import Plane


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
    assert context.page.status_code == 201
    
@then("The head is in the same place as before")
def step_impl(context):
    head = (context.plane.coor_x, context.plane.coor_y)
    assert head == (7,4)
