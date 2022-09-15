import ast
import datetime
import json

from flask import url_for

from app import db
from app.daos.user_dao import add_user
from app.models.user import Profile, User


@given("there is a Users with Profile")
def step_impl(context):
    user = User(username="Jhon", email="jhon@email", password="pass")
    db.session.add(user)
    db.session.commit()

    dob = datetime.datetime(2002, 3, 3, 10, 10, 10)
    profile = Profile(dob=dob, job="developer", user=user)
    db.session.add(profile)
    db.session.commit()

    context.user = user
    assert True


@when("we query the user information")
def step_impl(context):
    context.page = context.client.get(
        url_for("users.get_user", user_id=context.user.id)
    )
    assert context.page.status_code == 200


@then("I would like to see the Profile information")
def step_impl(context):
    raw_expected = {
        "email": "jhon@email",
        "id": 1,
        "profile": {"dob": "2002-03-03T10:10:10", "id": 1, "job": "developer"},
        "username": "Jhon",
    }

    raw_response = ast.literal_eval(context.page.text)

    response, expected = json.dumps(raw_response, sort_keys=True), json.dumps(
        raw_expected, sort_keys=True
    )

    assert response == expected
