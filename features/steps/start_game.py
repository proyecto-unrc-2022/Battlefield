from behave import *
from flask import url_for
import json
from app.models.navy.dynamic_navy_models import Game
from app.navy.navy_constants import PATH_TO_START
from app.navy.navy_game_control import NavyGameControl
from app.models.user import User
from app.daos.user_dao import add_user
from app import db

@given(u'I am logged in as "user1"')
def step_impl(context):
    add_user("user1","12345","user1@user1.com")
    context.user_1 = User.query.filter_by(username="user1").first()
    assert context.user_1.email == "user1@user1.com"


@given(u'the app has been initialized')
def step_impl(context):
    assert context.client

    
@given(u'I have some ships available')
def step_impl(context):
    context.available_ships = NavyGameControl.read_data(PATH_TO_START)
    assert context.available_ships

@when(u'I request to create a game')
def step_impl(context):
    context.headers = {"Content-Type":"application/json"}
    context.body = {"id_user_1":context.user_1.id}
    context.page = context.client.post(url_for("navy.create_game"),json=context.body,headers= 
    context.headers)
    assert context.page

@then(u'I should get the available ships and the game id')
def step_impl(context):
    data = json.loads(context.page.text)
    ships = context.available_ships 
    ships['game_id'] = Game.query.filter_by(id_user_1=context.user_1.id).first().id

    assert data == ships
   
    

