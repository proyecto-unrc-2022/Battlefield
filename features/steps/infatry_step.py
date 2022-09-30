from app import db 
from app.models.infantry.infantry_game import Figure_infantry, Game_Infantry
from app.models.user import Profile

from flask import url_for

from app.models.user import User
from app.daos.user_dao import add_user

@given('a user Ignacio')
def step_impl(context):
    user = User(username= "Ignacio", email="Ignacio@gmail.com", password="123")
    add_user(user.username, user.password, user.email)
    assert True

@when('you choose your soldier')
def step_impl(context):
    context.page = context.client.post(url_for("infantry.choose_entity",entity_id= 1))
    assert context.page.status_code == 200
    
@then('the soldier is created')
def step_impl(context):
    ob = Figure_infantry.query.order_by(Figure_infantry.id.desc()).first()
    context.ob = ob
    is_created = context.ob.id == 1
    is_soldier = Figure_infantry.query.filter_by(id=1).first().type_figure == 1
    assert is_created and is_soldier

@given('a user Matias')
def step_impl(context):
    user = User(username= "Matias", email="Matias@gmail.com", password="123")
    add_user(user.username, user.password, user.email)
    assert True

@when('you choose your Humvee')
def step_impl(context):
    context.page = context.client.post(url_for("infantry.choose_entity",entity_id= 2))
    assert context.page.status_code == 200
    
@then('the humvee is created')
def step_impl(context):
    ob = Figure_infantry.query.order_by(Figure_infantry.id.desc()).first()
    context.ob = ob
    is_created = context.ob.id == 2
    is_humvee = Figure_infantry.query.filter_by(id=2).first().type_figure == 2
    assert is_created and is_humvee



@given('a user Lucas')
def step_given(context) :
    user = User(username= "Lucas", email="Lucas@gmail.com", password="1234")
    add_user(user.username, user.password, user.email)
    assert True   
    
@when('you choose your tank')
def step_when(context) :
    context.page = context.client.post(url_for("infantry.choose_entity",entity_id= 3))
    assert context.page.status_code == 200
    
@then('the tank is created')
def step_then(context) :
    ob = Figure_infantry.query.order_by(Figure_infantry.id.desc()).first()
    context.ob = ob
    is_created = context.ob.id == 3
    is_tank = Figure_infantry.query.filter_by(id=3).first().type_figure == 3
    assert is_created and is_tank


  
@given('a user Ricardo')
def step_given(context) :
    user = User(username= "Ricardo", email="Ricardo@gmail.com", password="1324")
    add_user(user.username, user.password, user.email)
    assert True   

@when('you choose your artillery')
def step_when(context) :
    context.page = context.client.post(url_for("infantry.choose_entity",entity_id=4))
    assert context.page.status_code == 200 

@then('the artillery is created')
def step_then(context) :
    ob = Figure_infantry.query.order_by(Figure_infantry.id.desc()).first()
    context.ob = ob
    is_created = context.ob.id == 4
    is_artillery = Figure_infantry.query.filter_by(id=4).first().type_figure == 4
    assert is_created and is_artillery