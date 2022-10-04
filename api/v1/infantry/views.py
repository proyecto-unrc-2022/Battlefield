from api import token_auth

from app import db

from flask import Response, request

from app.daos.infantry.infantry_dao import add_entity
from app.daos.infantry.infantry_dao import create_game
from app.daos.infantry.infantry_dao import ready
from app.daos.infantry.infantry_dao import join
from app.daos.infantry.infantry_dao import move_by_user
from app.daos.infantry.infantry_dao import is_valid_move


from . import infantry

@infantry.route("/game/<user_id>",methods=['POST'])
def start_game(user_id):

    if(create_game(user_id) != None):
        return Response(status=200)
    else:
        return Response(status=404)
    

@infantry.route("/start/<game_id>",methods=['POST'])
def ready_to_play(game_id):
    if (ready(game_id)):
        return Response(status=200)
    else:
        return Response(status=404)

@infantry.route("/start/<game_id>/<user_id>",methods=['POST'])
def join_game(game_id, user_id):
    if (join(game_id, user_id)):
        return Response(status=200)
    else:
        return Response(status=404)        

@infantry.route("/create_entity/<user_id>/<entity_id>",methods=['POST'])
def choose_entity(user_id ,entity_id):
    if (add_entity(user_id ,entity_id)):
        return Response(status=200)
    else:
        return Response(status=404)

@infantry.route("/action/<direction>/<velocity>/<user_id>",methods=['POST'])
def mov_action(direction, velocity, user_id):
    if(is_valid_move(move_by_user(user_id, direction, velocity))):
        return Response(status=200)
    else:
        return Response(status=404)


    
# Routes here
