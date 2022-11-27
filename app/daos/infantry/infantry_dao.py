from telnetlib import GA
from app import db
from app.models.user import Profile
from sqlalchemy import insert, select, update
from ...models.infantry.figure_infantry import Figure_Infantry_Schema, Figure_infantry
from ...models.infantry.game_Infantry import Game_Infantry
from ...models.infantry.projectile_infantry import Projectile_infantry
from ...models.user import User
from .constant import *
import queue



import copy
queue_turn = None
players_actions = None
projectile_queue = None
def add_figure(game_id, user_id ,entity_id, position_X, position_Y):
    
    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()

    if(not(validation_create(game_id, user_id))):
        return None

    diccionary_figure = {1:{"hp":10,"velocidad":3,"tamaño":1,"direccion":2,"type":SOLDIER},
                        2:{"hp":20,"velocidad":5,"tamaño":2,"direccion":2,"type":HUMVEE},
                        3:{"hp":50,"velocidad":2,"tamaño":3,"direccion":2,"type":TANK},
                        4:{"hp":80,"velocidad":1,"tamaño":4,"direccion":2,"type":ARTILLERY}}
    
    if(int(entity_id) < 1 or int(entity_id) > 4):    
        return None
        
    figure = Figure_infantry(id_game= game_id, id_user= user_id, 
                            hp=diccionary_figure[entity_id]["hp"], 
                            velocidad=diccionary_figure[entity_id]["velocidad"], 
                            tamaño=diccionary_figure[entity_id]["tamaño"], 
                            direccion=diccionary_figure[entity_id]["direccion"], 
                            pos_x=position_X, 
                            pos_y=position_Y, 
                            type=diccionary_figure[entity_id]["type"])
    
    succes = validation_position(game_id, user_id, figure)

    if(not(succes)):
        return None

    if(figure):
        db.session.add(figure)
        db.session.commit()
    else:
        figure = None
    
    return figure

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
        object.direccion = 6

    return succes

def validation_figure(object):

    succes = False

    if(0 <= object.pos_x <= 19 and 0 <= object.pos_y <= 9):
        
        succes = True
    
    return succes


def validation_create(game_id, user_id):

    """
    Dado un game_id y un user_id, verifica que el creador de un projectile o figure es un user del game
    Args:
        game_id (int) id del juego
        user_id (int) id del usuario
    Return:
        boolean: (True si el user que pertenece a un juego, crea un shoot/figure de ese game)
    """

    game = db.session.query(Game_Infantry).filter_by(id = game_id).first()

    if(game.id_user2 != None):
        if(game.id_user1 == int(user_id) or game.id_user2 == int(user_id)):
            return True       
    return False

def move_save(game_id, user_id, direction, velocity):
    """Guarda el movimiento realizado en una cola llamada players_actions

    Args:
        game_id (int): id del juego
        user_id (int): id del usuario
        direction (int): direccion a la que se movera la unidad
        velocity (int): cantidad de casillas que se va a mover su unidad
     Returns:
        boolean: True si se guardo el movimiento, False si es que sucedio algos
    """
    global players_actions
    success = False 
    figure = db.session.query(Figure_infantry).filter_by(id_user = user_id, id_game = game_id).first()
    aux_figure = copy.copy(figure)
    game = Game_Infantry.query.filter_by(id = game_id).first()
    exceeded_velocity_limit = (velocity > figure.velocidad)
    for i in range(velocity):
        coor = direc(direction, aux_figure.pos_x, aux_figure.pos_y)
        aux_figure.pos_x = aux_figure.pos_x + (aux_figure.pos_x - coor[0])
        aux_figure.pos_y = aux_figure.pos_y + (aux_figure.pos_y - coor[1])
    if not(exceeded_velocity_limit) and validation_figure(aux_figure):
        assis_server_restart(game)
        players_actions.put(("move", game_id, user_id, direction, velocity))
        reduce_action(figure.id)
        success = True
    return success

def move(game_id, user_id, direction, velocity):
    """Dado un user_id, una direccion y una velocidad, mueva su respectiva unidad en el juego
    Args:
        game_id (int): id del juego
        user_id (int): id del usuario
        direction (int): direccion a la que se movera la unidad
        velocity (int): cantidad de casillas que se va a mover su unidad
    Returns:
        boolean: (No colisiona con otra figure) y (no excede su limite)
    """
    collision = False
    figures = figures_id_game(game_id)
    figure = db.session.query(Figure_infantry).filter_by(id_user = user_id, id_game = game_id).first()
    figure_opponent = Figure_infantry.query.filter_by(id_user = find_opponent(game_id, figure.id), id_game = game_id).first()
    aux_figure = copy.copy(figure)
    exceeded_velocity_limit = (velocity > figure.velocidad)
    for i in range(velocity):
        coor = direc(direction, aux_figure.pos_x, aux_figure.pos_y)
        aux_figure.pos_x = aux_figure.pos_x + (aux_figure.pos_x - coor[0])
        aux_figure.pos_y = aux_figure.pos_y + (aux_figure.pos_y - coor[1])
        collision = False if aux_figure == None else intersection([aux_figure.pos_x, aux_figure.pos_y], figures[(figure_opponent.id)-1][1]) or collision
    if not(collision) and not(exceeded_velocity_limit): 
        db.session.query(Figure_infantry).filter(
            Figure_infantry.id_user == user_id, Figure_infantry.id_game == game_id).update(
                {'pos_x' :  aux_figure.pos_x, 'pos_y' : aux_figure.pos_y, 'direccion' : direction})

    elif collision and not(exceeded_velocity_limit):
        db.session.query(Figure_infantry).filter(
            Figure_infantry.id == figure.id).update(
                {'hp' :  figure.hp - figure_opponent.hp})
        if(not(figure.hp - figure_opponent.hp > 0)):    
            db.session.query(Figure_infantry).filter(
                Figure_infantry.id == figure_opponent.id).update(
                    {'hp' :  figure_opponent.hp - figure.hp})
    db.session.commit()
    return not(collision) and not(exceeded_velocity_limit) 

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
    return user_opponent.id


def intersection(coord1, coords2):
    """Verifica la interseccion de un par ordenado con un grupo de par ordenados

    Args:
        coord1 (list): par de coordenada (x,y)
        coords2 (list): grupo de par coordenado [(x,y)]

    Returns:
        bool: Si hay interseccion retorna True
    """
    intersection = False
    for j in range(len(coords2)):
        for i in range(len(coord1)-1):
            if coord1 == list(coords2[j]):
                intersection = True
    return intersection


def shoot_save(user_id, game_id, direccion, velocity):
    """Guarda el movimiento realizado en una cola llamada players_actions

    Args:
        user_id (int): user id de quien dispara
        game_id (int): game id de donde se dispara
        direccion (int): direccion de a donde se dispara
    Returns:
        bool: True si se guardo el disparo, False si ocurrio algo
    """
    global players_actions
    game = Game_Infantry.query.filter_by(id = game_id).first()
    figure = Figure_infantry.query.filter_by(id_game= game_id, id_user= user_id).first()
    if(not(validation_create(game_id, user_id))):
        return False
    projectile = Projectile_infantry(id_game= game_id, 
                                pos_x=0, 
                                pos_y=0, 
                                velocidad=velocity, 
                                daño=0, 
                                direccion= direccion,
                                type=MISSILE)
    if(not(validation_figure(direction_of_projectile(figure, projectile, direccion)))):
        return False
    else:
        assis_server_restart(game)
        players_actions.put(("shoot", user_id, game_id, direccion, velocity))
        reduce_action(figure.id)
    return True


#Primero busca en la tabla Figura el personaje del usuario.
#Luego pregunta si la direccion que quiere disparar es verdadero o no.
#Si el disparo se puede realizar, pregunta cual es la figure y dependiendo cual es crea su respectivo proyectil. 
def shoot(user_id, game_id, direccion, velocity):

    figure = Figure_infantry.query.filter_by(id_game= game_id, id_user= user_id).first()
        
    if(figure_valid(figure, game_id, direccion, velocity)):
        return True
    else:
        return False

#Este metodo es la creacion para los proyectiles
def figure_valid(figure, game_id, direccion, velocity):

    diccionary_projectile1 = {1:{"velocidad":0,"daño":1},
                              2:{"velocidad":0,"daño":2},
                              3:{"velocidad":0,"daño":5}}

    diccionary_projectile2 = {2:{"velocidad":5,"daño":5},
                              3:{"velocidad":3,"daño":15},
                              4:{"velocidad":velocity,"daño":30}}
    
    y = 1
    
    if(figure.figure_type == SOLDIER):
        aux_figure = copy.copy(figure)
        while y != 4:
            projectile = Projectile_infantry(id_game= game_id, 
                                    pos_x=0, 
                                    pos_y=0, 
                                    velocidad=diccionary_projectile1[y]["velocidad"], 
                                    daño=diccionary_projectile1[y]["daño"], 
                                    direccion= direccion,
                                    type=MACHINE_GUN)
            direction_of_projectile(aux_figure, projectile, direccion)
            figure.direccion = direccion
            db.session.add(figure)
            db.session.add(projectile)
            db.session.commit()
            aux_figure.pos_x = projectile.pos_x
            aux_figure.pos_y = projectile.pos_y
            y = y + 1
        return True
    elif(figure.figure_type == HUMVEE or figure.figure_type == TANK):
        projectile = Projectile_infantry(id_game= game_id, 
                                pos_x=0, 
                                pos_y=0, 
                                velocidad=diccionary_projectile2[figure.figure_type]["velocidad"], 
                                daño=diccionary_projectile2[figure.figure_type]["daño"], 
                                direccion= direccion,
                                type=MISSILE)
        direction_of_projectile(figure, projectile, direccion)
        figure.direccion = direccion
        db.session.add(figure)
        db.session.add(projectile)
        db.session.commit()
        return True
    elif(figure.figure_type == ARTILLERY):
        if((velocity < 3 or velocity > 20)):
            return False
        else:
            projectile = Projectile_infantry(id_game= game_id, 
                                pos_x=0, 
                                pos_y=0, 
                                velocidad=diccionary_projectile2[figure.figure_type]["velocidad"], 
                                daño=diccionary_projectile2[figure.figure_type]["daño"], 
                                direccion= direccion,
                                type=MORTAR)
            direction_of_projectile(figure, projectile, direccion)
            figure.direccion = direccion
            db.session.add(figure)
            db.session.add(projectile)
            db.session.commit()
            return True
    else:
        return False

    

#Este metodo toma la figura y el proyectil.
#Setea las posiciones x e y para la creacion de los proyectiles
def direction_of_projectile(figure, projectile, direccion):
    if(direccion == 0):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)
    elif(direccion == 1):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)
    elif(direccion == 2):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)
    elif(direccion == 3):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)
    elif(direccion == 4):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)
    elif(direccion == 5):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)
    elif(direccion == 6):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)
    elif(direccion == 7):
        projectile.pos_x = figure.pos_x + (COORDS_CUERPO[direccion][0] * -1)
        projectile.pos_y = figure.pos_y + (COORDS_CUERPO[direccion][1] * -1)

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
    assis_server_restart(game)
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
    if queue_turn == None: queue_turn = queue.Queue()
    if game.turn == None :
        turn_list = list(queue_turn.queue)
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
        next_turn(game_id) (llamada 3) - retorna True
    2° ronda:
        next_turn(game_id) (llamada 4) - 1° turno: user2
        next_turn(game_id) (llamada 5) - 2° turno: user1
        next_turn(game_id) (llamada 6) - retorna True
    Args:
        game (Game_Infantry): game en el que se quiere avanzar el turno

    Returns:
        bool: True si la ronda termino, False si la ronda aun no termino y avanza el turno
    """

    global queue_turn
    round = False
    figure_user1 = Figure_infantry.query.filter_by(id_user = game.id_user1).first()
    figure_user2 = Figure_infantry.query.filter_by(id_user = game.id_user2).first()
    assis_server_restart(game)
    current_figure = Figure_infantry.query.filter_by(id_user = game.turn).first()
    if queue_turn.empty() and (current_figure.avail_actions == 0 or current_figure.avail_actions == None):
        #Cuando ya no hay mas turnos en la ronda
        queue_turn.put(find_opponent(game.id, User.query.filter_by(id = game.turn).first().id))
        round = True
        db.session.query(Figure_infantry).filter(
            Figure_infantry.id_user == figure_user1.id, Figure_infantry.id_game == game.id).update(
                {'avail_actions' : 1})
        db.session.query(Figure_infantry).filter(
            Figure_infantry.id_user == figure_user2.id, Figure_infantry.id_game == game.id).update(
                {'avail_actions' : 1})
        db.session.query(Game_Infantry).filter(
            Game_Infantry.id == game.id).update(
                {'turn' :  game.turn})
    elif current_figure.avail_actions == 0:
        #Cuando falta algun turno en la ronda
        db.session.query(Game_Infantry).filter(
            Game_Infantry.id == game.id).update(
                {'turn' :  queue_turn.get()})
    db.session.commit()
    return round

def move_projectile(projectile_id, game_id):
    """Mueve el proyectil, y si colisiona se destruye

    Args:
        projectile_id (int): id del projectil a mover
        game_id (int): id del game donde pertenece el projectil
    Returns:
        lista: retorna True si el proyectil se movio, o False si el proyectil se destruyo
    """
    projectile = Projectile_infantry.query.filter_by(id = projectile_id, id_game = game_id).first()
    figures = figures_id_game(game_id)
    move = True
    pos = (projectile.pos_x, projectile.pos_y)
    if projectile.type == MACHINE_GUN:
        projectile_collision(projectile, game_id)
        damage_Projectile(projectile, figures)
        db.session.delete(projectile)
    elif projectile.type == MISSILE:       
        if not(projectile_collision(projectile, game_id)) or not(damage_Projectile(projectile, figures)):
            for i in range(projectile.velocidad):
                pos = direc(projectile.direccion, pos[0], pos[1])
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
            pos = direc(projectile.direccion, pos[0], pos[1])
        projectile.pos_x = projectile.pos_x + (projectile.pos_x - pos[0])
        projectile.pos_y = projectile.pos_y + (projectile.pos_y - pos[1])
        if projectile_collision(projectile, game_id): 
            move = False
        elif damage_Projectile(projectile, figures): 
            move = False
        db.session.delete(projectile)    
    if move :
        db.session.query(Projectile_infantry).filter(
            Projectile_infantry.id == projectile_id, Projectile_infantry.id_game == game_id).update(
                {'pos_x' :  projectile.pos_x, 'pos_y' : projectile.pos_y, 'direccion' : projectile.direccion})
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
    projectiles = Projectile_infantry.query.filter_by(id_game = game_id).all()
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

    game = db.session.query(Projectile_infantry).filter_by(id= projectile_id).first().id_game
    figure_1 = db.session.query(Figure_infantry).filter_by(id_game= game).first().id
    #figure_2 = db.session.query(Figure_infantry).filter_by(id_game= game).type

    damage_user(projectile_id, figure_1)
    #damage_projectile(projectile_id, user_2)
    
    
#Borrar
def damage_user(projectile_id, figure):

    projectileId = db.session.query(Projectile_infantry).filter_by(id= projectile_id).first()

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

    projectile = db.session.query(Projectile_infantry).filter_by(id= projectile_id).first()

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
    game = db.session.query(Projectile_infantry).id_game
    other_projectile = db.session.query(Projectile_infantry).order_by(id_game= game).id

    if(projectile_id.pos_x == other_projectile.pos_x and projectile_id.pos_y == other_projectile.pos_y):
        db.session.query(Projectile_infantry).filter_by(id= other_projectile).destroy
        db.session.query(Projectile_infantry).filter_by(id= projectile_id).destroy

def direc(dir, pos_x, pos_y):

    if dir in COORDS_CUERPO:
        return (pos_x + COORDS_CUERPO[dir][0], pos_y + COORDS_CUERPO[dir][1])

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

    return figures

def damage_Projectile(projectile, figures):
    projectile_pos = (projectile.pos_x, projectile.pos_y)
    damage = False
    for x in figures.values():
        if(projectile_pos in x[1]):
            x[0].hp = x[0].hp - projectile.daño
            db.session.add(x[0])
            db.session.delete(projectile)
            db.session.commit()
            damage = True
    return damage

def intersec_Projectile_all(game_id):

    projectile_all = Projectile_infantry.query.filter_by(id_game = game_id).all()

    figures = figures_id_game(game_id)

    pos = None

    if(projectile_all != None):
        for i in range(len(projectile_all)):
            pos = damage_Projectile(projectile_all[i], figures)
    return pos

def is_your_turn(game_id, user_id):
    """Indica si es su turno

    Args:
        game_id (int): id del game en el que se vera si es su turno
        user_id (int): id del user en el que se vera si es su turno

    Returns:
        bool: True si es el turno de ese user, False si no es su turno 
    """
    figure = Figure_infantry.query.filter_by(id_game = game_id, id_user = user_id).first()
    game = Game_Infantry.query.filter_by(id = game_id).first()
    is_your_turn = True
    if figure.avail_actions == 0 or game.turn != user_id: is_your_turn = False
    return is_your_turn

def reduce_action(figure_id):
    """Reduce la acciones disponibles de una fiura

    Args:
        figure_id (int): figura a la que se le reducira la accion
    """
    db.session.query(Figure_infantry).filter(
            Figure_infantry.id_user == figure_id).update(
                {'avail_actions' : 0})
    db.session.commit()
    
def assis_server_restart(game):
    """Es como una asistencia por si se reinicia el servidero y poder continuar el juego normalmente.
    Cuando se reinicia el servidor en medio de una ronda, la ronda se reinicia por completo perdiendo
    las jugadas hechas previamente

    Args:
        game (Game_Infrantry): instancia del juego a verificar posibles problemas
    """
    global queue_turn
    global players_actions
    figure_user1 = Figure_infantry.query.filter_by(id_user = game.id_user1).first()
    figure_user2 = Figure_infantry.query.filter_by(id_user = game.id_user2).first()
    if(queue_turn == None and game.id_user2 == None):
        queue_turn = queue.Queue()
        queue_turn.put(game.id_user1)
    elif queue_turn == None and game.turn != None:
        queue_turn = queue.Queue()
        if figure_user1.avail_actions == 1 and figure_user2.avail_actions == 0: 
            game.turn = game.id_user2
            db.session.query(Game_Infantry).filter(
            Game_Infantry.id == game.id).update(
            {'turn' : game.id_user2})
        if figure_user1.avail_actions == 0 and figure_user2.avail_actions == 1:
            game.turn = game.id_user1
            db.session.query(Game_Infantry).filter(
            Game_Infantry.id == game.id).update(
            {'turn' : game.id_user1})
        queue_turn.put(find_opponent(game.id, User.query.filter_by(id = game.turn).first().id))
        db.session.query(Figure_infantry).filter(
        Figure_infantry.id_user == figure_user1.id, Figure_infantry.id_game == game.id).update(
            {'avail_actions' : 1})
        db.session.query(Figure_infantry).filter(
        Figure_infantry.id_user == figure_user2.id, Figure_infantry.id_game == game.id).update(
            {'avail_actions' : 1})
        db.session.commit()
    if players_actions == None: 
        players_actions = queue.Queue()

def update_projectile(game):
    """Actualiza un proyectil diferente cada vez que se invoca siguiendo el orden especificado en 
       la narrativa
    Args:
        game (Game_Infantry): game de donde se actualizaran los proyectiles
    Returns:
        Projectile_Infantry: retorna el projectil que se actualizo, si no se actualizo ningun projectil
        retorna None
    """
    global projectile_queue
    update = True
    projectile = None
    if projectile_queue == None:
        #Carga la cola con los proyectiles actualmente en el juego
        machine_gun_queue = queue.Queue()
        projectile_queue = queue.Queue()
        projectiles = Projectile_infantry.query.filter_by(id_game = game.id).order_by(Projectile_infantry.id.asc()).all()
        for projectil in projectiles:
            if projectil.type == MACHINE_GUN: 
                #Los proyectiles tipo MACHINE_GUN van a una cola aparte, para luego
                #ser agregadas al final de la cola de projectile_queue
                machine_gun_queue.put(projectil.id)
            else:
                projectile_queue.put(projectil.id)
        for i in range(machine_gun_queue.qsize()):
            projectile_queue.put(machine_gun_queue.get())
    if projectile_queue.qsize() == 0: 
        #Cuando ya no hay mas proyectiles en la cola
        update = False
        projectile_queue = None   
    if(projectile_queue != None):
        #Saca un proyectil de la cola y lo mueve
        while projectile == None:
            projectile_id = projectile_queue.get()
            projectile = Projectile_infantry.query.filter_by(id = projectile_id, id_game = game.id).first()
        print(projectile.pos_x, projectile.pos_y)
        move_projectile(projectile_id, game.id)
        print(projectile.pos_x, projectile.pos_y)
        if((projectile.pos_x < 0 or projectile.pos_x > 20) or (projectile.pos_y < 0 or projectile.pos_y > 10)):
            db.session.delete(projectile)
            db.session.commit()
    return projectile
             
def update_users():
    """Realiza una accion a la vez de la cola players_actions, es decir, desencola una accion y para que
        vuelva a desencolar otra accion se tiene que volver a llamar el metodo

    Returns:
        bool: True si se realizo alguna accion, False en caso contrario
    """
    global players_actions
    succes = False
    if players_actions.qsize() == 0:
        succes = False
    else:
        action = players_actions.get()
        if action[0] == "move":
            if move(action[1], action[2], action[3], action[4]) : succes = True
        elif action[0] == "shoot":
            if shoot(action[1], action[2], action[3], action[4]) : succes= True
    return succes

def game_over(game):
    """Verifica si hay un ganador

    Args:
        game (Game_Infantry): el game donde se verifica si hay un ganador

    Returns:
        bool: Devuelve True si hay un ganador, si no, devuelve False
    """
    figure1 = db.session.query(Figure_infantry).filter_by(id_user = game.id_user1, id_game = game.id).first()
    figure2 = db.session.query(Figure_infantry).filter_by(id_user = game.id_user2, id_game = game.id).first()
    return figure1.hp < 0 or figure2.hp < 0

def update(game_id):
    game = Game_Infantry.query.filter_by(id = game_id).first()
    assis_server_restart(game)
    there_is_a_winner = game_over(game)
    if next_turn(game) and not(there_is_a_winner): 
        update_proj = True
        while update_proj: update_proj = update_projectile(game) #misiles y morteros 1°
        update_users() #posicion y/o creacion de proyectiles 3°
        update_users()
    #pos = intersec_Projectile_all(game_id)
    return there_is_a_winner



def removeGame(game_id):

    game = Game_Infantry.query.filter_by(id = game_id).first()
    db.session.delete(game)
    db.session.commit()

    return True