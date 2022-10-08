from telnetlib import GA
#from turtle import left, right
from app import db
from app.models.user import Profile
from ...models.infantry.infantry_game import Figure_infantry
from ...models.infantry.infantry_game import Game_Infantry
from ...models.infantry.infantry_game import Projectile
from ...models.user import User
from sqlalchemy import update
from .direction import *
import copy

def  add_figure(game_id, user_id ,entity_id):

    succes = True
    if("1" == entity_id):
        soldier = Figure_infantry(id_game= game_id, id_user= user_id, hp=10, velocidad=3, tamaño=1, direccion=0,pos_x=0, pos_y=0, type=1)
        db.session.add(soldier)
        db.session.commit()
    elif("2" == entity_id):
        humvee = Figure_infantry(id_game= game_id, id_user= user_id, hp=20, velocidad=5, tamaño=2, direccion=0, pos_x=0, pos_y=0, type=2)
        db.session.add(humvee)
        db.session.commit()
    elif("3" == entity_id):
        tank = Figure_infantry(id_game= game_id, id_user= user_id, hp=50, velocidad=2, tamaño=3, direccion=0, pos_x=0, pos_y=0, type=3)
        db.session.add(tank)
        db.session.commit()
    elif("4" == entity_id):
        artillery = Figure_infantry(id_game= game_id, id_user= user_id, hp=80, velocidad=1, tamaño=4, direccion=0,pos_x=0, pos_y=0, type=4)
        db.session.add(artillery)
        db.session.commit()
    else:
        succes = False
    return succes


#Dado un user_id, una direccion y una velocidad, mueva su respectiva unidad en el juego
#velocity seria la cantidad de casillas que se va a mover su unidad
#verificando que no supere su velocidad maxima.
#ej: la velocidad limite del tanque es 2, entonces su velocity no puede ser mayor a 2
def move_by_user(game_id, user_id, direction, velocity):
    figure = Figure_infantry.query.filter_by(id_user = user_id, id_game = game_id).first()
    aux_figure = copy.copy(figure)
    exceeded_velocity_limit = (int(velocity) > figure.velocidad)
    move(aux_figure, int(direction), int(velocity))
    is_valid = False if aux_figure == None else is_valid_move(aux_figure)
    if is_valid : 
        figure.pos_x = Figure_infantry.pos_x + aux_figure.pos_x
        figure.pos_y = Figure_infantry.pos_y + aux_figure.pos_y
        db.session.commit() 
    print(is_valid)
    return is_valid and not(exceeded_velocity_limit)

#Verifica que si una unidad(figure) se movio, este movimiento se valido
#devuelve verdadero si la unidad que se movio no choca contra otra unidad
def is_valid_move(figure):

    game_id = Figure_infantry.query.filter_by(id_game = figure.id_game).first().id_game
    game = Game_Infantry.query.filter_by(id = game_id).first()
    user_1 = game.user_1
    user_2 = game.user_2
    opponent = user_1 if user_1.id != figure.id else user_2
    figure_opponent = Figure_infantry.query.filter_by(id_user = opponent.id, id_game = game_id).first()
    return not(intersection(copy.copy(figure), copy.copy(figure_opponent)))

#Verifica si hay una interseccion entre dos figure
def intersection(figure_1, figure_2):

    intersection = False
    for i in range(figure_1.tamaño):
        aux_figure = copy.copy(figure_2)
        for j in range(figure_2.tamaño):
            equal_pos_x = figure_1.pos_x == aux_figure.pos_x
            equal_pos_y = figure_1.pos_y == aux_figure.pos_y
            intersection = equal_pos_x and equal_pos_y
            aux_figure = move(aux_figure, aux_figure.direccion, j)
        figure_1 = move(figure_1, figure_1.direccion, i)
    return intersection

#Devuelve un figure con la direccion y velocidad que se
#pasaron por parametros
def move(figure, direction, velocity):
    if(direction == EAST):
        figure.direccion = EAST
        figure.pos_x = figure.pos_x + velocity
    elif(direction == SOUTH_EAST):
        figure.direccion = SOUTH_EAST
        figure.pos_x = figure.pos_x + velocity
        figure.pos_y = figure.pos_y - velocity
    elif(direction == SOUTH):
        figure.direccion = SOUTH
        figure.pos_y = figure.pos_y - velocity
    elif(direction == SOUTH_WEST):
        figure.direccion = SOUTH_WEST
        figure.pos_x = figure.pos_x - velocity
        figure.pos_y = figure.pos_y - velocity
    elif(direction == WEST):
        figure.direccion = WEST
        figure.pos_x = figure.pos_x - velocity
    elif(direction == NORTH_WEST):
        figure.direccion = NORTH_WEST
        figure.pos_x = figure.pos_x + velocity
        figure.pos_y = figure.pos_y + velocity
    elif(direction == NORTH):
        figure.direccion = NORTH
        figure.pos_y = figure.pos_y + velocity
    else:
        return None
    return figure

#Primero busca en la tabla Figura el personaje del usuario.
#Luego pregunta si la direccion que quiere disparar es verdadero o no.
#Si el disparo se puede realizar, pregunta cual es la figure y dependiendo cual es crea su respectivo proyectil. 
def shoot(direction,figure_id,game_id):
 
    if (direction):
        if(figure_valid(figure_id,direction,game_id)):
            return True
        else:
            return False
    else:
        return False

#Este metodo verifica si la firura es valida.
def figure_valid(figure,direction,game_id):
    if(figure == "1"):
        projectile = Projectile(id_game= game_id, pos_x=0, pos_y=0, velocidad=0, daño=5, direccion= direction)
        db.session.add(projectile)
        db.session.commit()
        return True
    elif(figure == "2"):
        projectile = Projectile(id_game= game_id, pos_x=0, pos_y=0, velocidad=5, daño=5, direccion= direction)
        db.session.add(projectile)
        db.session.commit()
        return True
    elif(figure == "3"):
        projectile = Projectile(id_game= game_id, pos_x=0, pos_y=0, velocidad=3, daño=15, direccion= direction)
        db.session.add(projectile)
        db.session.commit()
        return True
    elif(figure == "4"):
        projectile = Projectile(id_game= game_id, pos_x=0, pos_y=0, velocidad=20, daño=30, direccion= direction)
        db.session.add(projectile)
        db.session.commit()
        return True
    else:
        return False

#Este metodo nos devuelve si la direccion es valida.
def shoot_valid(direction):

    if(direction == EAST or direction == SOUTH_EAST or direction == SOUTH_WEST or direction == NORTH or direction == NORTH_EAST or direction == NORTH_WEST or direction == SOUTH or direction == WEST):
        return True
    else:
        return False
           
def create_game(user_id):

    game = Game_Infantry(id_user1= user_id, id_user2= None)
    db.session.add(game)
    db.session.commit()
    return db.session.query(Game_Infantry).order_by(Game_Infantry.id.desc()).first().id  

def join(game_id, user_id):
    
    user = db.session.query(Game_Infantry).filter_by(id = game_id).first()

    if (user.id_user2 == user_id or user.id_user2 == None):

        game = db.session.query(Game_Infantry).get(game_id)
        game.id_user2 = user_id
        db.session.add(game)
        db.session.commit()
        return True
    
    return False

#Tira error 500 cuando entra al
def ready(game_id):

    if((db.session.query(Game_Infantry).get(game_id).id_user1 != None) or (db.session.query(Game_Infantry).get(game_id).id_user2 != None)):
        return True
    
    
    return False
