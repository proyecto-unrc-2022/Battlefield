import ast
import json

from flask import url_for

from app.daos.airforce.plane_dao import add_plane
from app.models.airforce.plane import Plane


@given("A  plane with information")
def step_impl(context):
    context.plane = add_plane(
        name="Hawker Tempest",
        size=1,
        speed=5,
        health=10,
        course=3,
        coor_x=3,
        coor_y=3
    )


@when("We query the plane information")
def step_impl(context):
    context.page = context.client.get(
        url_for("air_force.get_plane", plane_id=context.plane.id)
    )
    print(context.page.status_code)
    assert context.page.status_code is 200


@then("We see the information from the plane")
def step_impl(context):
    raw_expected = {
        "name": "Hawker Tempest",
        "size": 1,
        "speed": 5,
        "health": 10,
        "course": 3,
        "coor_x": 3,
        "coor_y":3
    }

    raw_response = ast.literal_eval(context.page.text)

    response, expected = json.dumps(raw_response, sort_keys=True), json.dumps(
        raw_expected, sort_keys=True
    )
    assert response == expected
