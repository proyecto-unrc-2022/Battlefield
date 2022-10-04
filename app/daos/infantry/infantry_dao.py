from telnetlib import GA
#from turtle import left, right
from app import db
from app.models.user import Profile
from ...models.infantry.infantry_game import Figure_infantry
from ...models.infantry.infantry_game import Game_Infantry
from ...models.infantry.infantry_game import Projectile
from ...models.user import User
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
#velocity seria la cantidad de casillas que se va a mover su unidad
#verificando que no supere su velocidad maxima.
#ej: la velocidad limite del tanque es 2, entonces su velocity no puede ser mayor a 2
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

def shoot(direction,user_id):
    user = db.session.query(User).filter_by(id= user_id)
    game = db.session.query(Game_Infantry).filter_by(id_user= user_id)
    figure = db.session.query(Figure_infantry).filter_by(id_user= user)
    if(direction == EAST and figure == "Soldier"):
        figure.direction=EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=0, daño=5, direccion=EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == EAST and figure == "Humvee"):
        figure.direction=EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=5, daño=5, direccion=EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == EAST and figure == "Tank"):
        figure.direction=EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=15, direccion=EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == EAST and figure == "Artillery"):
        figure.direction=EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=30, direccion=EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH and figure == "Soldier"):
        figure.direction=SOUTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=0, daño=5, direccion=SOUTH)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH and figure == "Humvee"):
        figure.direction=SOUTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=5, daño=5, direccion=SOUTH)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH and figure == "Tank"):
        figure.direction=SOUTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=15, direccion=SOUTH)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH and figure == "Artillery"):
        figure.direction=SOUTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=30, direccion=SOUTH)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_EAST and figure == "Soldier"):
        figure.direction=SOUTH_EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=0, daño=5, direccion=SOUTH_EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_EAST and figure == "Humvee"):
        figure.direction=SOUTH_EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=5, daño=5, direccion=SOUTH_EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_EAST and figure == "Tank"):
        figure.direction=SOUTH_EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=15, direccion=SOUTH_EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_EAST and figure == "Artillery"):
        figure.direction=SOUTH_EAST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=30, direccion=SOUTH_EAST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_WEST and figure == "Soldier"):
        figure.direction=SOUTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=0, daño=5, direccion=SOUTH_WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_WEST and figure == "Humvee"):
        figure.direction=SOUTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=5, daño=5, direccion=SOUTH_WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_WEST and figure == "Tank"):
        figure.direction=SOUTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=15, direccion=SOUTH_WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == SOUTH_WEST and figure == "Artillery"):
        figure.direction=SOUTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=30, direccion=SOUTH_WEST)
        db.session.add(projectile)
        db.session.commit()
     elif(direction == WEST and figure == "Soldier"):
        figure.direction=WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=0, daño=5, direccion=WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == WEST and figure == "Humvee"):
        figure.direction=WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=5, daño=5, direccion=WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == WEST and figure == "Tank"):
        figure.direction=WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=15, direccion=WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == WEST and figure == "Artillery"):
        figure.direction=WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=30, direccion=WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH_WEST and figure == "Soldier"):
        figure.direction=NORTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=0, daño=5, direccion=NORTH_WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH_WEST and figure == "Humvee"):
        figure.direction=NORTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=5, daño=5, direccion=NORTH_WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH_WEST and figure == "Tank"):
        figure.direction=NORTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=15, direccion=NORTH_WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH_WEST and figure == "Artillery"):
        figure.direction=NORTH_WEST
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=30, direccion=NORTH_WEST)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH and figure == "Soldier"):
        figure.direction=NORTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=0, daño=5, direccion=NORTH)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH and figure == "Humvee"):
        figure.direction=NORTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=5, daño=5, direccion=NORTH)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH and figure == "Tank"):
        figure.direction=NORTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=15, direccion=NORTH)
        db.session.add(projectile)
        db.session.commit()
    elif(direction == NORTH and figure == "Artillery"):
        figure.direction=NORTH
        projectile = Projectile(id_game= game, pos_x= , pos_y=, velocidad=3, daño=30, direccion=NORTH)
        db.session.add(projectile)
        db.session.commit()
        
    
        



def create_game(user_id):

    game = Game_Infantry(id_user1= user_id, id_user2= None)
    db.session.add(game)
    db.session.commit()
    return db.session.query(Game_Infantry).order_by(Game_Infantry.id.desc()).first().id  

def join(game_id, user_id):
    
    if (db.session.query(Game_Infantry).get(game_id)):
        game = db.session.query(Game_Infantry).get(game_id)
        game.id_user2 = user_id
        db.session.add(game)
        db.session.commit()
        return True
    else:
        return False

def ready(game_id):

    if(db.session.query(Game_Infantry).get(1).id_user1 == None or db.session.query(Game_Infantry).get(1).id_user2 == None):
        return False
    else:
        return True