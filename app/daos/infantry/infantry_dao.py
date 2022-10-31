from math import fabs
from telnetlib import GA
from app import db
from app.models.user import Profile
from sqlalchemy import insert, select, update
from ...models.infantry.figure_infantry import Figure_Infantry_Schema, Figure_infantry
from ...models.infantry.game_Infantry import Game_Infantry
from ...models.infantry.projectile_infantry import Projectile
from ...models.user import User
from .constant import *
import queue



import copy
queue_turn = None
def add_figure(game_id, user_id ,entity_id, position_X, position_Y):
    
    succes = validation_position(game_id, user_id, position_X, position_Y)

    if(not(succes)):
        return None

    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()


    diccionary_figure = {"1":{"hp":10,"velocidad":3,"tamaño":1,"direccion":0,"type":SOLDIER},
                        "2":{"hp":20,"velocidad":5,"tamaño":2,"direccion":1,"type":HUMVEE},
                        "3":{"hp":50,"velocidad":2,"tamaño":3,"direccion":0,"type":TANK},
                        "4":{"hp":80,"velocidad":1,"tamaño":4,"direccion":0,"type":ARTILLERY}}
    
    
    figure = Figure_infantry(id_game= game_id, id_user= user_id, 
                            hp=diccionary_figure[entity_id]["hp"], 
                            velocidad=diccionary_figure[entity_id]["velocidad"], 
                            tamaño=diccionary_figure[entity_id]["tamaño"], 
                            direccion=diccionary_figure[entity_id]["direccion"], 
                            pos_x=position_X, 
                            pos_y=position_Y, 
                            type=diccionary_figure[entity_id]["type"])

    if(game.id_user2 == int(user_id)):
        figure.direccion = 4 

    if(figure):
        db.session.add(figure)
        db.session.commit()
    else:
        figure = None
    
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
    user_opponent = find_opponent(game_id, figure.id)
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

def find_opponent(game_id, user_id):
    """Encuentra el oponente de la id de la figura dada por parametro

    Args:
        game_id (int): id del juego para buscar el oponente
        user_id (int): la id de la figura a la que se quiere encontrar el oponente

    Returns:
        int: id del oponente
    """
    game = Game_Infantry.query.filter_by(id = game_id).first()
    user_1 = game.user_1
    user_2 = game.user_2
    user_opponent = user_1 if user_1.id != user_id else user_2
    return user_opponent


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
def shoot(user_id, game_id, direccion):

    figure = Figure_infantry.query.filter_by(id_game= game_id, id_user= user_id).first()

    if(figure_valid(figure, game_id, direccion)):

        return True
    else:
        return False

#Este metodo es la creacion para los proyectiles
def figure_valid(figure, game_id, direccion):

    diccionary_projectile1 = {1:{"velocidad":0,"daño":5},
                              2:{"velocidad":0,"daño":2},
                              3:{"velocidad":0,"daño":1}}

    diccionary_projectile2 = {2:{"velocidad":5,"daño":5},
                              3:{"velocidad":3,"daño":15},
                              4:{"velocidad":20,"daño":30}}
    
    y = 1
    if(figure.figure_type == SOLDIER):
        while y != 4:
            projectile = Projectile(id_game= game_id, 
                                    pos_x=0, 
                                    pos_y=0, 
                                    velocidad=diccionary_projectile1[y]["velocidad"], 
                                    daño=diccionary_projectile1[y]["daño"], 
                                    direccion= direccion,
                                    type=MACHINE_GUN)
            direction_of_projectile(figure, projectile, direccion)
            db.session.add(projectile)
            db.session.commit()
            figure.pos_x = projectile.pos_x
            figure.pos_y = projectile.pos_y
            y = y + 1
        return True
    else:
        projectile = Projectile(id_game= game_id, 
                                pos_x=0, 
                                pos_y=0, 
                                velocidad=diccionary_projectile2[figure.figure_type]["velocidad"], 
                                daño=diccionary_projectile2[figure.figure_type]["daño"], 
                                direccion= direccion,
                                type=MISSILE)
        direction_of_projectile(figure, projectile, direccion)
        db.session.add(projectile)
        db.session.commit()
        return True
        
    return False

#Este metodo toma la figura y el proyectil.
#Setea las posiciones x e y para la creacion de los proyectiles
def direction_of_projectile(figure, projectile, direccion):
    print(direccion)
    if(direccion == 0):
        projectile.pos_x = figure.pos_x + COORDS[direccion+4][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion+4][1]
    elif(direccion == 1):
        projectile.pos_x = figure.pos_x + COORDS[direccion+2][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion+2][1]
    elif(direccion == 2):
        projectile.pos_x = figure.pos_x + COORDS[direccion][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion][1]
    elif(direccion == 3):
        projectile.pos_x = figure.pos_x + COORDS[direccion-2][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion-2][1]
    elif(direccion == 4):
        projectile.pos_x = figure.pos_x + COORDS[direccion-4][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion-4][1]
    elif(direccion == 5):
        projectile.pos_x = figure.pos_x + COORDS[direccion+2][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion+2][1]
    elif(direccion == 6):
        projectile.pos_x = figure.pos_x + COORDS[direccion][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion][1]
    elif(direccion == 7):
        projectile.pos_x = figure.pos_x + COORDS[direccion-2][0]
        projectile.pos_y = figure.pos_y + COORDS[direccion-2][1]

    return projectile

    
def create_game(user_id):
    global queue_turn
    game = Game_Infantry(id_user1= user_id, id_user2= None)
    db.session.add(game)
    db.session.commit()
    queue_turn = queue.Queue()
    queue_turn.put(user_id)
    return game  

def join(game_id, user_id):
    global queue_turn
    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()
    if (game != None and game.id_user2 == None):
        game.id_user2 = user_id
        db.session.add(game)
        db.session.commit()
        queue_turn.put(user_id)
        return True
    
    return False

def ready(game_id, user_id):
    """Verifica que ambos jugadores esten listos para jugar antes de empezar la partida

    Args:
        game_id (int): id del game al que se jugara
        user_id (int): id del usuario que marco que ya esta listo para jugar

    Returns:
        bool: si ambos jugadores estan listos para jugar retorna True
    """
    global queue_turn
    is_players_ready = False
    game = Game_Infantry.query.filter_by(id = game_id).first()
    if game.turn == None :
        turn_list = queue_turn.queue
        if (user_id in turn_list) and len(turn_list) > 0:
            turn_list.remove(user_id)
            queue_turn.queue = queue.deque(turn_list)
        if len(turn_list) == 0: 
            queue_turn = queue.Queue()
            game.turn = game.id_user1
            next_turn(game)
    if game.turn != None: is_players_ready = True
    return is_players_ready

def next_turn(game):
    """Avanza el turno solo si LA RONDA NO A TERMINADO,
    cuando la ronda termina, se crea de nuevo 2 turnos donde se respeta el orden
    explicado en la narrativa. Ej:
    1° ronda:
        next_turn(game_id) (llamada 1) - 1° turno: user1
        next_turn(game_id) (llamada 2) - 2° turno: user2
        next_turn(game_id) (llamada 3) - retrona True
    2° ronda:
        next_turn(game_id) (llamada 4) - 1° turno: user2
        next_turn(game_id) (llamada 5) - 2° turno: user1
        next_turn(game_id) (llamada 6) - retrona True
    Args:
        game (Game_Infantry): game en el que se quiere avanzar el turno

    Returns:
        bool: True si la ronda termino, False si la ronda aun no termino y avanza el turno
    """
    global queue_turn
    round = False
    if queue_turn == None and game.turn != None: #Este caso es por si el servidor se reinicia, pueda retomar los turnos
        queue_turn = Queue() 
        queue_turn.put(game.turn)
    if queue_turn.empty():
        queue_turn.put(game.turn)
        queue_turn.put(find_opponent(game.id, User.query.filter_by(id = game.turn).first().id).id)
        round = True
        db.session.query(Game_Infantry).filter(
            Game_Infantry.id == game.id).update(
                {'turn' :  game.turn})
    else: 
        available_action = 1
        db.session.query(Game_Infantry).filter(
            Game_Infantry.id == game.id).update(
                {'turn' :  queue_turn.get()})
    db.session.commit()
    return round

def move_projecile(projectile_id, game_id, direction):
    """Mueve el proyectil, y si colisiona se destruye

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
    pos = (projectile.pos_x, projectile.pos_y)
    if projectile.type == MACHINE_GUN:
        projectile_collision(projectile_id, game_id)
        damage_Projectile(projectile, figures)
        db.session.delete(projectile)
    elif projectile.type == MISSILE:       
        for i in range(projectile.velocidad):
            pos = direc(direction, pos[0], pos[1])
            projectile.pos_x = projectile.pos_x + (projectile.pos_x - pos[0])
            projectile.pos_y = projectile.pos_y + (projectile.pos_y - pos[1])
            pos = (projectile.pos_x, projectile.pos_y)
            if projectile_collision(projectile, game_id):
                move = False
                break
            elif damage_Projectile(projectile, figures): 
                move = False
                break
    elif projectile.type == MORTAR:
        for i in range(projectile.velocidad):
            pos = direc(direction, pos[0], pos[1])
        projectile.pos_x = projectile.pos_x + (projectile.pos_x - pos[0])
        projectile.pos_y = projectile.pos_y + (projectile.pos_y - pos[1])
        if damage_Projectile(projectile, figures): 
            move = False
        elif damage_Projectile(projectile, figures): 
            move = False
        db.session.delete(projectile)    
    if move :
        db.session.query(Projectile).filter(
            Projectile.id == projectile_id, Projectile.id_game == game_id).update(
                {'pos_x' :  projectile.pos_x, 'pos_y' : projectile.pos_y, 'direccion' : direction})
        db.session.commit()
    return move

def projectile_collision(projectile, game_id):
    """detecta si el proyectil dado se colisiona con los del resto del juego y los
        proyectiles colisionados los elimina

    Args:
        projectile (Proyectile): proyectil al que se le va a detectar la colision con el resto del juego
        game_id (int): id del juego en el que se hara dicha deteccion

    Returns:
        bool: retrona True si hubo una colision, si no retorna False
    """
    collision = False
    projectile_pos = (projectile.pos_x, projectile.pos_y)
    projectiles = Projectile.query.filter_by(id_game = game_id).all()
    for i in range(len(projectiles)):
        opponent_projectil_pos = (projectiles[i].pos_x, projectiles[i].pos_y)
        if (projectile_pos == opponent_projectil_pos) and (projectile.id != projectiles[i].id):
            db.session.delete(projectiles[i])
            collision = True
    if collision: 
        db.session.delete(projectile)
        db.session.commit()
    return collision           
        

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

def validation_position(game_id, user_id, object):

    succes = False

    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()

    if(game.id_user1 == int(user_id)):
        if(0 <= object.pos_x <= 9 and 0 <= object.pos_y <= 10):
            
            succes = True

    if(game.id_user2 == int(user_id)):
        if(11 <= object.pos_x <= 20 and 0 <= object.pos_y <= 10):
            
            succes = True

    if(game.id_user2 == int(user_id)):
        object.direccion = 2

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



