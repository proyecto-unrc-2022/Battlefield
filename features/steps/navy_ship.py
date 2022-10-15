import json

from behave import *
from flask import url_for

from app import db
from app.daos.user_dao import add_user
from app.models.user import User


@given("I've created a Navy Game")
def step_impl(context):
    pass


@given("another user joins the game I've created")
def step_impl(context):
    pass


@when("I try to create a \"Destroyer\" ship in ('2', '3') position, and 'N' direction")
def step_impl(context):
    pass


@then("the ship should be created successfully")
def step_impl(context):
    pass


@given("another user creates a Navy Game")
def step_impl(context):
    pass


@given("I join the game created by another user")
def step_impl(context):
    pass


@when("I try to create a \"Destroyer\" ship in ('5', '17') coords, and 'N' direction")
def step_impl(context):
    pass


@when("I try to create ship with wrong name or course")
def step_impl(context):
    pass


@when("I try to create ship with ('11', '9') coords")
def step_impl(context):
    pass


@when("I try to create ship with ('2', '16') coords")
def step_impl(context):
    pass


@when("I try to create ship with ('2', '6') coords")
def step_impl(context):
    pass
