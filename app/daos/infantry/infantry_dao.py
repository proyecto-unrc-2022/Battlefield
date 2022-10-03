from telnetlib import GA
from turtle import left, right
from app import db
from app.models.user import Profile
from ...models.infantry.infantry_game import Figure_infantry
from ...models.infantry.infantry_game import Game_Infantry
from .direction import *

def  add_entity(entity_id):
    succes = True
    if("1" == entity_id):
        soldier = Figure_infantry(hp=10, velocidad=3, tamaño=1, direccion=0,pos_x=0, pos_y=0, type=1)
        db.session.add(soldier)
        db.session.commit()
    elif("2" == entity_id):
        humvee = Figure_infantry(hp=20, velocidad=5, tamaño=2, direccion=0, pos_x=0, pos_y=0, type=2)
        db.session.add(humvee)
        db.session.commit()
    elif("3" == entity_id):
        tank = Figure_infantry(hp=50, velocidad=2, tamaño=3, direccion=0, pos_x=0, pos_y=0, type=3)
        db.session.add(tank)
        db.session.commit()
    elif("4" == entity_id):
        artillery = Figure_infantry(hp=80, velocidad=1, tamaño=4, direccion=0,pos_x=0, pos_y=0, type=4)
        db.session.add(artillery)
        db.session.commit()
    else:
        succes = False
    return succes


#Dado un user_id, una direccion y una velocidad, mueva su respectiva unidad en el juego
def move_by_user(user_id, direction, velocity):
    game_id = Game_Infantry.query.order_by(Game_Infantry.id.desc()).first().id
    figure = Figure_infantry.query.filter_by(id_user = user_id, id_game = game_id).first()
    exceeded_velocity_limit = (velocity <= figure.velocidad)   
    return (mov(figure, direction, velocity) != None) and exceeded_velocity_limit

#Verifica que si una unidad(figure) se movio, este movimiento se valido
#devuelve verdadero si la unidad que se movio no choca contra otra unidad
def is_valid_move(figure):
    game_id = Game_Infantry.query.order_by(Game_Infantry.id.desc()).first().id
    user_1 = Game_Infantry.query.order_by(Game_Infantry.id.desc()).first().user_1
    user_2 = Game_Infantry.query.order_by(Game_Infantry.id.desc()).first().user_2
    opponent = user_1 if user_1.id != figure.id else user_2
    figure_opponent = Figure_infantry.query.filter_by(id_user = opponent.id, id_game = game_id).first()
    return intersection(figure, figure_opponent)

#Verifica si hay una interseccion entre dos figure
def intersection(figure_1, figure_2):
    intersection = False
    for i in range(figure_1.tamaño):
        aux_figure = figure_2
        figure_1 = mov(figure_1, figure_1.direction, i)
        for j in range(figure_2.tamaño):
            equal_pos_x = figure_1.pos_x == aux_figure.pos_x
            equal_pos_y = figure_1.pos_y == aux_figure.pos_y
            intersection = equal_pos_x and equal_pos_y
            aux_figure = mov(aux_figure, aux_figure.direction, j)
    return intersection

#Devuelve un figure con la direccion y velocidad que se
#pasaron por parametros
def mov(figure, direction, velocity):
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
        figure.pos_x = figure.pos_x - velocity
        figure.pos_y = figure.pos_y + velocity
    elif(direction == NORTH):
        figure.direccion = NORTH
        figure.pos_x = figure.pos_x - velocity
        figure.pos_y = figure.pos_y + velocity
    else:
        return None
    return figure


def create_game(user_id):

    game = Game_Infantry(id_user1= user_id, id_user2= None)
    db.session.add(game)
    db.session.commit()
    return db.session.query(Game_Infantry).order_by(Game_Infantry.id.desc()).first().id  

def join(game_id, user_id):
    
    if (db.session.query(Game_Infantry).get(game_id)):
        game = db.session.query(Game_Infantry).get(game_id)
        game.id_user2 = user_id
        return True
    else:
        return False

def ready(game_id):

    if(db.session.query(Game_Infantry).get(1).id_user1 == None or db.session.query(Game_Infantry).get(1).id_user2 == None):
        return False
    else:
        return True