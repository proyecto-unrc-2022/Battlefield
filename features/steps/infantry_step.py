import json
from flask import url_for

from app import db
from app.daos.infantry.constant import *
from app.daos.user_dao import add_user
from app.models.infantry.projectile_infantry import Projectile_infantry
from app.models.infantry.figure_infantry import Figure_infantry
from app.models.infantry.game_Infantry import Game_Infantry
from app.models.user import Profile, User


@given('the first player Franco')
def step_impl(context):
    user1 = User(username= "Franco", email="Franco@gmail.com", password="123")
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Franco", "email" : "Franco@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you create the game')
def step_impl(context):
    context.page = context.client.post(url_for("infantry.start_game",user_id= 1))
    assert context.page.status_code == 200

@then('it is the first player')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.ready_to_play"), data = json.dumps(
        {"game_id" : 1, "user_id" : 1}), headers=headers)
    assert context.page.status_code == 200

@given('the second player Tomas')
def step_impl(context):
    user2 = User(username= "Tomas", email="Tomas@gmail.com", password="123")
    add_user(user2.username, user2.password, user2.email)
    context.user = user2
    assert True

@when('he joins the game')
def step_impl(context):
    game = Game_Infantry(id_user1= 1, id_user2= None)
    db.session.add(game)
    db.session.commit()  
    context.page = context.client.post(url_for("infantry.join_game",game_id= 1, user_id= 2))
    assert context.page.status_code == 200

@then('he is the second player')
def step_impl(context):
    game = Game_Infantry.query.filter_by(id = 1).first()
    assert game.id_user2 == 2
    
# @given('a user Franco')
# def step_impl(context):
#     user1 = User(username= "Franco", email="Franco@gmail.com", password="123")
#     add_user(user1.username, user1.password, user1.email)
#     user2 = User(username= "Tomas", email="Tomas@gmail.com", password="123")
#     add_user(user2.username, user2.password, user2.email)
#     user = User.query.filter_by(id = 1).first()
#     assert not(user == None)

# @when('you choose your soldier')
# def step_impl(context):
#     context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= 1),
#         data = json.dumps({"pos_x" : 1, "pos_y" : 1}))
#     assert context.page.status_code == 200
    
# @then('the soldier is created')
# def step_impl(context):
#     ob = Figure_infantry.query.filter_by(id_user = 1, id_game = 1).first()
#     context.ob = ob
#     is_created = context.ob.id == 1
#     is_soldier = context.ob.figure_type == 1
#     assert is_created and is_soldier

# @given('a user Tomas')
# def step_impl(context):
#     user = user = User.query.filter_by(username = "Tomas").first()
#     assert not(user == None)

# @when('you choose your Humvee')
# def step_impl(context):
#     context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 2, figure_id= 2))
#     assert context.page.status_code == 200
    
# @then('the humvee is created')
# def step_impl(context):
#     ob = Figure_infantry.query.filter_by(id_user = 2, id_game = 1).first()
#     context.ob = ob
#     is_created = context.ob.id == 2
#     is_humvee = context.ob.figure_type == 2
#     assert is_created and is_humvee

# @given('a user Lucas')
# def step_given(context) :
#     user = User(username= "Lucas", email="Lucas@gmail.com", password="1234")
#     add_user(user.username, user.password, user.email)
#     assert True   
    
# @when('you choose your tank')
# def step_when(context) :
#     context.page = context.client.post(url_for("infantry.choose_entity",entity_id= 3))
#     assert context.page.status_code == 200
    
# @then('the tank is created')
# def step_then(context) :
#     ob = Figure_infantry.query.order_by(Figure_infantry.id.desc()).first()
#     context.ob = ob
#     is_created = context.ob.id == 3
#     is_tank = Figure_infantry.query.filter_by(id=3).first().figure_type == 3
#     assert is_created and is_tank
  
# @given('a user Ricardo')
# def step_given(context) :
#     user = User(username= "Ricardo", email="Ricardo@gmail.com", password="1324")
#     add_user(user.username, user.password, user.email)
#     assert True   

# @when('you choose your artillery')
# def step_when(context) :
#     context.page = context.client.post(url_for("infantry.choose_entity",entity_id=4))
#     assert context.page.status_code == 200 

# @then('the artillery is created')
# def step_then(context) :
#     ob = Figure_infantry.query.order_by(Figure_infantry.id.desc()).first()
#     context.ob = ob
#     is_created = context.ob.id == 4
#     is_artillery = Figure_infantry.query.filter_by(id=4).first().figure_type == 4
#     assert is_created and is_artillery


# @when('you choose to move your unit east')
# def step_when(context) :
#     context.page = context.client.post(url_for("infantry.mov_action", game_id = 1, user_id = 1, velocity = 2, direction = EAST))
#     assert context.page.status_code == 200    

# @then('the unit moves east')
# def step_then(context) :
#     figure = Figure_infantry.query.filter_by(id_game = 1, id_user = 1).first()
#     assert figure.pos_x == 2 and figure.pos_y == 0
    
# @when('you choose to move your unit west')
# def step_when(context) :
#     figure = Figure_infantry.query.filter_by(id_game = 1, id_user = 2).first()
#     context.page = context.client.post(url_for("infantry.mov_action", game_id = 1, user_id = 2, velocity = 2, direction = NORTH))
#     assert context.page.status_code == 200
    
# @then('the unit moves west')
# def step_then(context) :
#     figure = Figure_infantry.query.filter_by(id_game = 1, id_user = 2).first()
#     assert figure.pos_y == 2 and figure.pos_x == 0

# @when('choose an invalid move')
# def step_when(context) :
#     figure = Figure_infantry.query.filter_by(id_game = 1, id_user = 2).first()
#     context.page = context.client.post(url_for("infantry.mov_action", game_id = 1, user_id = 2, velocity = 2, direction = SOUTH_EAST))
#     assert context.page.status_code == 404

# @then('the unit does not move')
# def step_then(context) :
#     figure = Figure_infantry.query.filter_by(id_game = 1, id_user = 2).first()
#     assert figure.pos_y == 2 and figure.pos_x == 0

# @given('a user Nicolas')
# def step_given(context):
#     user = User(username= "Nicolas", email="Nicolas@gmail.com", password="123")
#     add_user(user.username, user.password, user.email)
#     context.user = user
#     assert True

# @when('Shoot')
# def step_when(context):
#     user2 = User(username= "Ignacio", email="Ignacio@gmail.com", password="123")
#     Figure_infantry(id_game= 1, id_user= 2, hp=10, velocidad=3, tamaño=1, direccion=0,pos_x=0, pos_y=0, type=1)
#     game = Game_Infantry(id_user1= context.user, id_user2= user2.id)
#     context.page = context.client.post(url_for("infantry.shoot_entity",direction= 1, figure_id=1, user_id= 2, game_id= 1))
#     print(context.page.status_code)
#     assert context.page.status_code == 200

  
# @then(u'create the projectile')
# def step_then(context) :
#     #figure = Figure_infantry.query.filter_by(id_game = 1, id_user = 1).first()
#     #assert figure.pos_x == 1
#     pass
 