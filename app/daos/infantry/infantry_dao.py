from turtle import left, right
from app import db
from app.models.user import Profile
from ...models.infantry.infantry_game import Figure_infantry
from ...models.infantry.infantry_game import Game_Infantry

EAST = 1
SOUTH_EAST = 2
SOUTH = 3
SOUTH_WEST = 4
WEST = 5
NORTH_WEST = 6
NORTH = 7

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

def move(user_id, direction, velocity):
    figure = Figure_infantry.query.filter_by(id_user = user_id).first()
    exceeded_velocity_limit = velocity <= figure.velocidad
    succes = True
    if(direction == EAST and exceeded_velocity_limit):
        figure.direccion = EAST
        figure.pos_x = figure.pos_x + velocity
        db.session.commit()
    elif(direction == SOUTH_EAST and exceeded_velocity_limit):
        figure.direccion = SOUTH_EAST
        figure.pos_x = figure.pos_x + velocity
        figure.pos_y = figure.pos_y - velocity
        db.session.commit()
    elif(direction == SOUTH and exceeded_velocity_limit):
        figure.direccion = SOUTH
        figure.pos_y = figure.pos_y - velocity
        db.session.commit()
    elif(direction == SOUTH_WEST and exceeded_velocity_limit):
        figure.direccion = SOUTH_WEST
        figure.pos_x = figure.pos_x - velocity
        figure.pos_y = figure.pos_y - velocity
        db.session.commit()
    elif(direction == WEST and exceeded_velocity_limit):
        figure.direccion = WEST
        figure.pos_x = figure.pos_x - velocity
        db.session.commit()
    elif(direction == NORTH_WEST and exceeded_velocity_limit):
        figure.direccion = NORTH_WEST
        figure.pos_x = figure.pos_x - velocity
        figure.pos_y = figure.pos_y + velocity
        db.session.commit()
    elif(direction == NORTH and exceeded_velocity_limit):
        figure.direccion = NORTH
        figure.pos_x = figure.pos_x - velocity
        figure.pos_y = figure.pos_y + velocity
        db.session.commit()
    else:
        succes = False;
    return succes