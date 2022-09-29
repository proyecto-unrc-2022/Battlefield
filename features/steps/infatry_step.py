from app import db 
from app.models.infantry.entity import Entity
from app.daos.infantry.entity_dao import add_entity

from flask import url_for

from app.models.user import User
from app.daos.user_dao import add_user

@given(u'a user Ignacio')
def step_impl(context):
    user = User(username= "Ignacio", email="Ignacio@gmail.com", password="123")
    add_user(user.username, user.password, user.email)
    assert True

@when(u'you choose your soldier')
def step_impl(context):
    user1 = db.session.query(User).filter_by()
    context.page = context.client.post(url_for("infantry.start_game",user_id= 1))
    assert context.page.status_code == 200
    
@then(u'the soldier is created')
def step_impl(context):
    ob = db.session.query(Entity).first()
    context.ob = ob
    assert context.ob.id == 1


@given(u'the first player')
def step_impl(context):
    user1 = User(username= "Franco", email="Franco@gmail.com", password="123")
    add_user(user1.username, user1.password, user1.email)
    context.user = user1
    assert True

@when(u'they press play')
def step_impl(context):
    context.page = context.client.post(url_for("infantry.start_game",user_id= 1))
    print(context.page.status_code)
    assert context.page.status_code == 200

@then(u'the game begins')
def step_impl(context):
    context.page = context.client.post(url_for("infantry.ready_to_play",game_id= 1))
    print(context.page.status_code)
    assert context.page.status_code == 404


######################## TERMINAR ESTOS ESCENARIOS, LUEGO DE LA OPCION #######################################33    
#
#@given(u'a user Matias')
#def step_impl(context):
#    user = User(username= "Matias", email="Matias@gmail.com", password="123")
#    add_user(user.username, user.password, user.email)
#    assert True
#
#@when(u'you choose your Humvee')
#def step_impl(context):
#    context.page = context.client.post(url_for("infantry.choose_entity",entity_id= 2))
#    assert context.page.status_code == 200
#
#@then(u'the humvee is created')
#def step_impl(context):
#    ob = db.session.query(Entity).filter_by()
#    context.ob = ob
#    assert context.ob.id == 2
#    