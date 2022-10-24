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
from .type import *
import copy

def add_figure(game_id, user_id ,entity_id):
    if(SOLDIER == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=10, velocidad=3, tamaño=1, direccion=0,pos_x=0, pos_y=0, type=1)
    elif(HUMVEE == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=20, velocidad=5, tamaño=2, direccion=0, pos_x=0, pos_y=0, type=2)
    elif(TANK == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=50, velocidad=2, tamaño=3, direccion=0, pos_x=0, pos_y=0, type=3)
    elif(ARTILLERY == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=80, velocidad=1, tamaño=4, direccion=0,pos_x=0, pos_y=0, type=4)
    else:
        figure = None
    if(figure):
        db.session.add(figure)
        db.session.commit()
    return figure


def move(game_id, user_id, direction, velocity):
    """Dado un user_id, una direccion y una velocidad, mueva su respectiva unidad en el juego

    Args:
        game_id (int): id del juego
        user_id (int): id del usuario
        direction (int): direccion a la que se movera la unidad
        velocity (int): cantidad de casillas que se va a mover su unidad

    Returns:
        boolean: (si el movimiento es valido) y (no excede su limite)
    """
    figure = db.session.query(Figure_infantry).filter_by(id_user = user_id, id_game = game_id).first()
    game = Game_Infantry.query.filter_by(id = game_id).first()
    user_1 = game.user_1
    user_2 = game.user_2
    user_opponent = user_1 if user_1.id != figure.id else user_2
    figure_opponent = Figure_infantry.query.filter_by(id_user = user_opponent.id, id_game = game_id).first()
    
    aux_figure = copy.copy(figure)
    exceeded_velocity_limit = (velocity > figure.velocidad)
    coor = move_pos([aux_figure.pos_x, aux_figure.pos_y], direction, velocity)
    aux_figure.pos_x = coor[0]
    aux_figure.pos_y = coor[1]

    is_valid = False if aux_figure == None else not(intersection(copy.copy(aux_figure), copy.copy(figure_opponent)))
    if is_valid and not(exceeded_velocity_limit): 
        db.session.execute(
            update(Figure_infantry)
            .where(Figure_infantry.id_user == user_id, Figure_infantry.id_game == game_id)
            .values(pos_x = aux_figure.pos_x, pos_y = aux_figure.pos_y, direccion = direction)
        )
    elif not(is_valid) and not(exceeded_velocity_limit):
        db.session.execute(
            update(Figure_infantry)
            .where(Figure_infantry.id_user == figure.id_user, Figure_infantry.id_game == game_id)
            .values(hp = figure.hp - figure_opponent.hp)
        )
        db.session.execute(
            update(Figure_infantry)
            .where(Figure_infantry.id_user == figure_opponent.id, Figure_infantry.id_game == game_id)
            .values(hp = figure_opponent.hp - figure.hp)
        )
    db.session.commit()
    return is_valid and not(exceeded_velocity_limit)

#Verifica si hay una interseccion entre dos figure
def intersection(figure_1, figure_2):
    intersection = False
    for i in range(figure_1.tamaño):
        if intersection : break
        coor = move_pos([figure_1.pos_x, figure_1.pos_y], figure_1.direccion, i)
        figure_1.pos_x = coor[0]
        figure_1.pos_y = coor[1]
        figure_2_aux = copy.copy(figure_2)
        for j in range(figure_2.tamaño):
            if intersection : break
            coor = move_pos([figure_2_aux.pos_x, figure_2_aux.pos_y], figure_2_aux.direccion, j)
            figure_2_aux.pos_x = coor[0]
            figure_2_aux.pos_y = coor[1]
            equal_pos_x = figure_1.pos_x == figure_2_aux.pos_x
            equal_pos_y = figure_1.pos_y == figure_2_aux.pos_y
            intersection = equal_pos_x and equal_pos_y
    print(intersection)
    return intersection

def move_pos(coor, direction, velocity):
    """Mueve un par de cordenadas a la direccion y numero de casillas
        especificadas

    Args:
        coor (list): Par x e y en una lista
        direction (int): direccion
        velocity (int): cantidad de casillas que se movera

    Returns:
        list: par coordenados movidos (devuelve una lista)
    """
    if(direction == EAST):
        coor[0] = coor[0] + velocity
    elif(direction == SOUTH_EAST):
        coor[0] = coor[0] + velocity
        coor[1] = coor[1] - velocity
    elif(direction == SOUTH):
        coor[1] = coor[1] - velocity
    elif(direction == SOUTH_WEST):
        coor[0] = coor[0] - velocity
        coor[1] = coor[1] - velocity
    elif(direction == WEST):
        coor[0] = coor[0] - velocity
    elif(direction == NORTH_WEST):
        coor[0] = coor[0] - velocity
        coor[1] = coor[1] + velocity
    elif(direction == NORTH):
        coor[1] = coor[1] + velocity
    elif(direction == NORTH_EAST):
        coor[0] = coor[0] + velocity
        coor[1] = coor[1] + velocity
    else:
        coor = None
    return coor

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
#Falta cambiar las posiciones de los tres projectiles
#TODO: Cambiar pos_x y pos_y
def figure_valid(figure_id,direction,game_id):
    if(figure_id == SOLDIER):
        figure = db.session.query(Figure_infantry).filter_by(id= figure_id).first()
        projectile1 = Projectile(id_game= game_id, pos_x=figure.pos_x + 3, pos_y=figure.pos_y + 3, velocidad=0, daño=5, direccion= direction)
        db.session.add(projectile1)
        db.session.commit()
        projectile2 = Projectile(id_game= game_id, pos_x=figure.pos_ + 2, pos_y=figure.pos_y + 2, velocidad=0, daño=5, direccion= direction)
        db.session.add(projectile2)
        db.session.commit()
        projectile3 = Projectile(id_game= game_id, pos_x=figure.pos_x + 1, pos_y=figure.pos_y + 1, velocidad=0, daño=5, direccion= direction)
        db.session.add(projectile3)
        db.session.commit()
        return True
    elif(figure_id == HUMVEE):
        figure = db.session.query(Figure_infantry).filter_by(id= figure_id).first()
        projectile = Projectile(id_game= game_id, pos_x=figure.pos_x + 1, pos_y=figure.pos_y + 1, velocidad=5, daño=5, direccion= direction)
        db.session.add(projectile)
        db.session.commit()
        return True
    elif(figure_id == TANK):
        figure = db.session.query(Figure_infantry).filter_by(id= figure_id).first()
        projectile = Projectile(id_game= game_id, pos_x=figure.pos_x + 1, pos_y=figure.pos_y + 1, velocidad=3, daño=15, direccion= direction)
        db.session.add(projectile)
        db.session.commit()
        return True
    elif(figure_id == ARTILLERY):
        figure = db.session.query(Figure_infantry).filter_by(id= figure_id).first()
        projectile = Projectile(id_game= game_id, pos_x=figure.pos_x + 1, pos_y=figure.pos_y + 1, velocidad=20, daño=30, direccion= direction)
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
    return game  

def join(game_id, user_id):
    
    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()

    if (game != None and game.id_user2 == None):

        #game = db.session.query(Game_Infantry).get(game_id)
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


#Este metodo toma los misiles del game y actuliza todos sus movimientos
#Falta diferenciar cual de los dos figures del game.
def update_projectile(projectile_id):

    game = db.session.query(Projectile).filter_by(id= projectile_id).first().id_game
    figure_1 = db.session.query(Figure_infantry).filter_by(id_game= game).first().id
    #figure_2 = db.session.query(Figure_infantry).filter_by(id_game= game).type

    damage_user(projectile_id, figure_1)
    #damage_projectile(projectile_id, user_2)
    
    
#Este metodo hace el daño al player
def damage_user(projectile_id, figure):

    projectileId = db.session.query(Projectile).filter_by(id= projectile_id).first()

    figure_1 = db.session.query(Figure_infantry).filter_by(id= figure).first() #toma uno

    if(projectileId.pos_x == figure_1.pos_x and projectileId.pos_y == figure_1.pos_y):
        
        figure_1.hp = figure_1.hp - projectileId.daño
        if(figure_1.hp <= 0):
            db.session.delete(figure_1)
            db.session.commit()
        else:
            db.session.add(figure_1)
            db.session.commit()
    else:
        projectile = return_direction(projectileId.id)
        db.session.add(projectile)
        db.session.commit()

#Este metodo te retorna la direccion
def return_direction(projectile_id):

    projectile = db.session.query(Projectile).filter_by(id= projectile_id).first()

    if(projectile.direction == EAST):
        projectile.pos_x = projectile.pos_x + 1 
    elif(projectile.direction == SOUTH_EAST):
        projectile.pos_x = projectile.pos_x + 1
        projectile.pos_y = projectile.pos_y - 1
    elif(projectile.direction == SOUTH):
        projectile.pos_y = projectile.pos_y - 1
    elif(projectile.direction == SOUTH_WEST):
        projectile.pos_x = projectile.pos_x - 1
        projectile.pos_y = projectile.pos_y - 1
    elif(projectile.direction == WEST):
        projectile.pos_x = projectile.pos_x - 1  
    elif(projectile.direction == NORTH_WEST):
        projectile.pos_x = projectile.pos_x - 1
        projectile.pos_y = projectile.pos_y + 1
    elif(projectile.direction == NORTH):
        projectile.pos_y = projectile.pos_y + 1
    elif(projectile.direction == NORTH_EAST):
        projectile.pos_x = projectile.pos_x + 1
        projectile.pos_y = projectile.pos_y + 1
    else:
        return None
    return projectile

#Este metodo hace daño entre los projectiles
def damage_projectile(projectile_id):
    game = db.session.query(Projectile).id_game
    projectile = db.session.query(Projectile).filter_by(id= projectile_id).first()
    other_projectile = db.session.query(Projectile).order_by(id_game= game).first()

    if(projectile.pos_x == other_projectile.pos_x and projectile.pos_y == other_projectile.pos_y):
        db.session.delete(projectile)
        db.session.commit()
        db.session.delete(other_projectile)
        db.session.commit()
        


