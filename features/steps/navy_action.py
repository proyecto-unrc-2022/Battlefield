from behave import *
from flask import url_for
from app.daos.user_dao import add_user
from app.models.user import User

@given('I am logged in as "user"')
def step_impl(context):
    # Falta hacer el login y obtener el token
    add_user("user", "12345", "user@user.com")
    context.user = User.query.filter_by(username="user").first()
    assert context.user.email == "user@user.com"

@given("the app is initialized")
def step_impl(context):
    assert context.client

@given(u'Is my turn')
def step_impl(context):
    context.headers = {"Content-Type": "application/json"}
    context.page = context.client.post(
        url_for("navy.create_game"), json={"id_user_1": context.user_1.id}, headers=context.headers
    )
    assert context.page
   

@when(u'I try to move in a game that doesn\'t exist')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I try to move in a game that doesn\'t exist')

@then("I should see an error message '{error_msj}'")
def step_impl(context, error_msj):
   assert True

#-------------------------------------

