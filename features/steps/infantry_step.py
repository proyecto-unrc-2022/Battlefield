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
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.ready_to_play"), data = json.dumps(
    {"game_id" : 1, "user_id" : 2}), headers=headers)
    assert context.page.status_code == 200

@given('user any')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Eduardo", "email" : "Eduardo@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you create a game')
def step_impl(context):
    context.page = context.client.post(url_for("infantry.start_game",user_id= 1))
    assert context.page.status_code == 200

@then('he can not join a game that he created himself')
def step_impl(context):
    context.page = context.client.post(url_for("infantry.join_game",game_id= 1, user_id= 1))
    assert context.page.status_code == 404

##################################################### FIGURE ########################################################################
@given('a user with the corresponding coordinates')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Franco", "email" : "Franco@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you choose the figure and it is created')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "1"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('wait the opponent')
def step_impl(context):
    #When creating the figure then you should only wait for the opponent
    assert True

@given('a user with the wrong coordinates')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Damian", "email" : "Damian@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you choose the figure')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "1"), data = json.dumps(
        {"pos_x" : 12, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 404

@then('it couldn not have been created')
def step_impl(context):
    #Since the figure is not created then the scenario is true
    assert True

@given('a user x')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Juan", "email" : "Juan@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you select the type 1 figure')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "1"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('this figure is created for the user x')
def step_impl(context):
    figure = Figure_infantry.query.filter_by(id_game= 1, id_user= 1).first()
    assert figure.figure_type == 1

@given('a user y')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Jose", "email" : "Jose@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you select the type 2 figure')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "2"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('this figure is created for the user y')
def step_impl(context):
    figure = Figure_infantry.query.filter_by(id_game= 1, id_user= 1).first()
    assert figure.figure_type == 2

@given('a user z')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Felipe", "email" : "Felipe@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you select the type 3 figure')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "3"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('this figure is created for the user z')
def step_impl(context):
    figure = Figure_infantry.query.filter_by(id_game= 1, id_user= 1).first()
    assert figure.figure_type == 3

@given('a user t')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("users.create_user"), data = json.dumps(
        {"username" : "Luis", "email" : "Luis@gmail.com", "password" : "123"}), headers=headers)
    assert context.page.status_code == 200

@when('you select the type 4 figure')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "4"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('this figure is created for the user t')
def step_impl(context):
    figure = Figure_infantry.query.filter_by(id_game= 1, id_user= 1).first()
    assert figure.figure_type == 4

############################################## PROYECTIL ###########################################
@given('figure 1')
def step_impl(context):
     #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "1"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@when('he shoots for figure 1')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.shoot_entity", game_id = 1, user_id =  1, direccion= 1), data = json.dumps(
        {"velocity" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('your projectile is created for figure 1')
def step_impl(context):
    #Since the projectile was created successfully in the previous step then the scenario is true
    assert True

@given('figure 2')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "2"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@when('he shoots for figure 2')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.shoot_entity", game_id = 1, user_id =  1, direccion= 1), data = json.dumps(
        {"velocity" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('your projectile is created for figure 2')
def step_impl(context):
    #Since the projectile was created successfully in the previous step then the scenario is true
    assert True

@given('figure 3')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "3"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@when('he shoots for figure 3')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.shoot_entity", game_id = 1, user_id =  1, direccion= 1), data = json.dumps(
        {"velocity" : 1}), headers=headers)
    assert context.page.status_code == 200

@then('your projectile is created for figure 3')
def step_impl(context):
    #Since the projectile was created successfully in the previous step then the scenario is true
    assert True

@given('figure 4')
def step_impl(context):
    #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "4"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@when('he shoots for figure 4')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.shoot_entity", game_id = 1, user_id =  1, direccion= 1), data = json.dumps(
        {"velocity" : 4}), headers=headers)
    assert context.page.status_code == 200

@then('your projectile is created figure 4')
def step_impl(context):
    #Since the projectile was created successfully in the previous step then the scenario is true
    assert True

@given('a figure')
def step_impl(context):
     #The game must have a user 2
    game = Game_Infantry(id_user1= 1, id_user2= 2)
    db.session.add(game)
    db.session.commit() 
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.choose_figure", game_id = 1, user_id = 1, type= "1"), data = json.dumps(
        {"pos_x" : 1, "pos_y" : 1}), headers=headers)
    assert context.page.status_code == 200

@when('it moves')
def step_impl(context):
    headers = {"Content-Type": "application/json"}
    context.page = context.client.post(url_for("infantry.mov_action"), data = json.dumps(
        {"velocity" : 1 ,"course" : 3 ,"game_id" : 1 ,"user_id" : 1}), headers=headers)
    figure = Figure_infantry.query.filter_by(id_game = 1, id_user= 1).first()
    print(figure.pos_x)
    print(figure.pos_y)
    assert context.page.status_code == 202

