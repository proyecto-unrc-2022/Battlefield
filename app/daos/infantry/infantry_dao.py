from math import fabs
from pickle import TRUE
from telnetlib import GA
from app import db
from app.models.user import Profile
from sqlalchemy import insert, select, update
from ...models.infantry.figure_infantry import Figure_infantry
from ...models.infantry.game_Infantry import Game_Infantry
from ...models.infantry.projectile_infantry import Projectile
from ...models.user import User
from .constant import *
import copy



def add_figure(game_id, user_id ,entity_id, position_X, position_Y):

    succes = validation_position(game_id, user_id, position_X, position_Y)

    if(not(succes)):
        return None

    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()

    if(SOLDIER == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=10, velocidad=3, tamaño=1, direccion=0, pos_x=position_X, pos_y=position_Y, type=1)
    elif(HUMVEE == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=20, velocidad=5, tamaño=2, direccion=0, pos_x=position_X, pos_y=position_Y, type=2)
    elif(TANK == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=50, velocidad=2, tamaño=3, direccion=0, pos_x=position_X, pos_y=position_Y, type=3)
    elif(ARTILLERY == entity_id):
        figure = Figure_infantry(id_game= game_id, id_user= user_id, hp=80, velocidad=1, tamaño=4, direccion=0,pos_x=position_X, pos_y=position_Y, type=4)
    else:
        figure = None

    if(game.id_user2 == int(user_id)):
        figure.direccion = 4

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
    is_valid = True
    figures = figures_id_game(game_id)
    figure = db.session.query(Figure_infantry).filter_by(id_user = user_id, id_game = game_id).first()
    game = Game_Infantry.query.filter_by(id = game_id).first()
    user_1 = game.user_1
    user_2 = game.user_2
    user_opponent = user_1 if user_1.id != figure.id else user_2
    figure_opponent = Figure_infantry.query.filter_by(id_user = user_opponent.id, id_game = game_id).first()
    aux_figure = copy.copy(figure)
    exceeded_velocity_limit = (velocity > figure.velocidad)
    for i in range(velocity):
        coor = direc(direction, aux_figure.pos_x, aux_figure.pos_y)
        aux_figure.pos_x = aux_figure.pos_x + (aux_figure.pos_x - coor[0])
        aux_figure.pos_y = aux_figure.pos_y + (aux_figure.pos_y - coor[1])
        is_valid = False if aux_figure == None else not(intersection([aux_figure.pos_x, aux_figure.pos_y], figures[(figure_opponent.id)-1][1]))
    if is_valid and not(exceeded_velocity_limit): 
        db.session.query(Figure_infantry).filter(
            Figure_infantry.id_user == user_id, Figure_infantry.id_game == game_id).update(
                {'pos_x' :  aux_figure.pos_x, 'pos_y' : aux_figure.pos_y, 'direccion' : direction})

    elif not(is_valid) and not(exceeded_velocity_limit):
        db.session.query(Figure_infantry).filter(
            Figure_infantry.id_user == user_id, Figure_infantry.id_game == game_id).update(
                {'hp' :  figure.hp - figure_opponent.hp})
        db.session.query(Figure_infantry).filter(
            Figure_infantry.id_user == user_id, Figure_infantry.id_game == game_id).update(
                {'hp' :  figure_opponent.hp - figure.hp})
    db.session.commit()
    return is_valid and not(exceeded_velocity_limit)


def intersection(coord1, coords2):
    intersection = False
    for j in range(len(coords2)):
        for i in range(len(coord1)-1):
            if coord1[i] in coords2[j] and coord1[i+1] in coords2[j]:
                intersection = True
    return intersection


#Primero busca en la tabla Figura el personaje del usuario.
#Luego pregunta si la direccion que quiere disparar es verdadero o no.
#Si el disparo se puede realizar, pregunta cual es la figure y dependiendo cual es crea su respectivo proyectil. 
def shoot(user_id,game_id, direction):

    figure = Figure_infantry.query.filter_by(id_game= game_id, id_user= user_id).first()
    
    if(figure_valid(figure, direction, game_id)):
        return True
    else:
        return False

#Este metodo verifica si la firura es valida.
def figure_valid(figure, direction, game_id):
    aux = copy.copy(figure)
    pos = direc(direction, aux.pos_x, aux.pos_y)
    pos = (aux.pos_x + (aux.pos_x - pos[0]), aux.pos_y + (aux.pos_y - pos[1]))
    print(pos)

    is_valid = True
    if figure.figure_type == SOLDIER:
        #Proyectil delantero del soldado
        projectile1 = Projectile(id_game= game_id, pos_x=pos[0], pos_y=pos[1], velocidad=0, daño=5, direccion= direction, type = MACHINE_GUN)
        db.session.add(projectile1)
        db.session.commit()
        #Proyectiles laterales del soldado
        #Proyectiles horizontales
        if direction == NORTH or direction == SOUTH: 
            pos = direc(WEST, aux.pos_x, aux.pos_y)
            pos = (aux.pos_x + (aux.pos_x - pos[0]), aux.pos_y + (aux.pos_y - pos[1]))
            projectile2 = Projectile(id_game= game_id, pos_x=pos[0], pos_y=pos[1], velocidad=0, daño=5, direccion= direction, type=MACHINE_GUN)
            db.session.add(projectile2)
            db.session.commit()
            pos = direc(EAST, aux.pos_x, aux.pos_y)
            pos = (aux.pos_x + (aux.pos_x - pos[0]), aux.pos_y + (aux.pos_y - pos[1]))
            projectile3 = Projectile(id_game= game_id, pos_x=pos[0], pos_y=pos[1], velocidad=0, daño=5, direccion= direction, type=MACHINE_GUN)
            db.session.add(projectile3)
            db.session.commit()
        #Proyectiles verticales
        elif direction == WEST or direction == EAST:
            pos = direc(NORTH, aux.pos_x, aux.pos_y)
            projectile2 = Projectile(id_game= game_id, pos_x=pos[0], pos_y=pos[1], velocidad=0, daño=5, direccion= direction, type=MACHINE_GUN)
            db.session.add(projectile2)
            db.session.commit()
            pos = direc(SOUTH, aux.pos_x, aux.pos_y)
            projectile3 = Projectile(id_game= game_id, pos_x=pos[0], pos_y=pos[1], velocidad=0, daño=5, direccion= direction, type=MACHINE_GUN)
            db.session.add(projectile3)
            db.session.commit()
    elif(figure.figure_type == HUMVEE):
        projectile = Projectile(id_game= game_id, pos_x=pos[0] , pos_y=pos[1], velocidad=5, daño=5, direccion= direction, type=MISSILE)
        db.session.add(projectile)
        db.session.commit()
    elif(figure.figure_type == TANK):
        projectile = Projectile(id_game= game_id, pos_x=pos[0], pos_y=pos[1], velocidad=3, daño=15, direccion= direction, type=MISSILE)
        db.session.add(projectile)
        db.session.commit()
    elif(figure.figure_type == ARTILLERY):
        projectile = Projectile(id_game= game_id, pos_x=pos[0], pos_y=pos[1], velocidad=20, daño=30, direccion= direction, type=MORTAR)
        db.session.add(projectile)
        db.session.commit()
    else:
        is_valid = False
    return is_valid

           
def create_game(user_id):

    game = Game_Infantry(id_user1= user_id, id_user2= None, turn= user_id)
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


def move_projecile(projectile_id, game_id, direction):
    """devuelve la posiciones por donde se mueve el projectil

    Args:
        projectile_id (int): id del projectil a mover
        game_id (int): id del game donde pertenece el projectil
        direction (int): hacia donde se movera el proyectil

    Returns:
        lista: retorna True si el proyectil se movio, o False si el proyectil se destruyo
    """
    projectile = Projectile.query.filter_by(id = projectile_id, id_game = game_id).first()
    figures = figures_id_game(game_id)
    move = True
    if projectile.type == MACHINE_GUN:
        damage_Projectile(projectile, figures)
    elif projectile.type == MISSILE:       
        for i in range(projectile.velocidad):
            pos = direc(direction, pos[0], pos[1])
            projectile.pos_x = pos[0]
            projectile.pos_y = pos[1]
            if damage_Projectile(projectile, figures): 
                move = False
                break
    elif projectile.type == MORTAR:
        for i in range(projectile.velocidad):
            pos = direc(direction, pos[0], pos[1])
        projectile.pos_x = pos[0]
        projectile.pos_y = pos[1]
        if damage_Projectile(projectile, figures): 
            move = False
    if move :
        db.session.query(Projectile).filter(
            Projectile.id == projectile_id, Projectile.id_game == game_id).update(
                {'pos_x' :  projectile.pos_x, 'pos_y' : projectile.pos_y, 'direccion' : direction})
        db.session.commit()
    return move

         
    

#Este metodo toma los misiles del game y actuliza todos sus movimientos
#Falta diferenciar cual de los dos figures del game.
def update_projectile(projectile_id):

    game = db.session.query(Projectile).filter_by(id= projectile_id).first().id_game
    figure_1 = db.session.query(Figure_infantry).filter_by(id_game= game).first().id
    #figure_2 = db.session.query(Figure_infantry).filter_by(id_game= game).type

    damage_user(projectile_id, figure_1)
    #damage_projectile(projectile_id, user_2)
    
    
#Borrar
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
    other_projectile = db.session.query(Projectile).order_by(id_game= game).id

    if(projectile_id.pos_x == other_projectile.pos_x and projectile_id.pos_y == other_projectile.pos_y):
        db.session.query(Projectile).filter_by(id= other_projectile).destroy
        db.session.query(Projectile).filter_by(id= projectile_id).destroy

def validation_position(game_id, user_id, pos_x, pos_y):

    succes = False

    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()

    if(game.id_user1 == int(user_id)):
        if(0 <= pos_x <= 9 and 0 <= pos_y <= 10):
            
            succes = True

    if(game.id_user2 == int(user_id)):
        if(11 <= pos_x <= 20 and 0 <= pos_y <= 10):
            
            succes = True

    return succes


def direc(dir, pos_x, pos_y):

    if dir in COORDS:
        return (pos_x + COORDS[dir][0], pos_y + COORDS[dir][1])

    return None

def getposition(object):

    position= []
    pos = (object.pos_x, object.pos_y)
    position.append(pos)

    for i in range(object.tamaño - 1):
        pos = direc(object.direccion, pos[0], pos[1])
        position.append(pos)
    

    return position


def figures_id_game(game_id):

    figures_all = Figure_infantry.query.filter_by(id_game = game_id).all()
    sizeFigures_all = len(figures_all)


    figures = {}

    for x in range(sizeFigures_all):
        figures.update({x : [figures_all[x], getposition(figures_all[x])]})


    print(figures)

    return figures

def damage_Projectile(projectile, figures):
    projectile_pos = (projectile.pos_x, projectile.pos_y)
    damage = False
    for x in figures.values():
        print(x)
        if(projectile_pos in x[1]):
            x[0].hp = x[0].hp - projectile.daño
            db.session.add(x[0])
            db.session.delete(projectile)
            db.session.commit()
            damage = True
    return damage

def intersec_Projectile_all(game_id):

    projectile_all = Projectile.query.filter_by(id_game = game_id).all()

    figures = figures_id_game(game_id)

    pos = None

    if(projectile_all != None):
        for i in range(len(projectile_all)):
            print(projectile_all[i])
            pos = damage_Projectile(projectile_all[i], figures)
    return pos


def update(game_id):
    pos = intersec_Projectile_all(game_id)
    return True
