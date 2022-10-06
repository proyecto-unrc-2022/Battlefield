from api import token_auth

from app import db

from flask import Response, request

from app.daos.infantry.infantry_dao import add_figure
from app.daos.infantry.infantry_dao import create_game
from app.daos.infantry.infantry_dao import ready
from app.daos.infantry.infantry_dao import join
from app.daos.infantry.infantry_dao import move_by_user
from app.daos.infantry.infantry_dao import shoot


from . import infantry

@infantry.route("/game/user/<user_id>",methods=['POST'])
def start_game(user_id):

    if(create_game(user_id) != None):
        return Response(status=200)
    else:
        return Response(status=404)
    

@infantry.route("/start/game/<game_id>",methods=['POST'])
def ready_to_play(game_id):
    if (ready(game_id)):
        return Response(status=200)
    else:
        return Response(status=404)

@infantry.route("/start/game/<game_id>/user/<user_id>",methods=['POST'])
def join_game(game_id, user_id):
    if (join(game_id, user_id)):
        return Response(status=200)
    else:
        return Response(status=404)        

@infantry.route("/create_entity/game/<game_id>/user/<user_id>/figure/<figure_id>",methods=['POST'])
def choose_figure(game_id, user_id ,figure_id):
    if (add_figure(game_id, user_id ,figure_id)):
        return Response(status=200)
    else:
        return Response(status=404)

@infantry.route("/action/game/<game_id>/course/<direction>/velocity/<velocity>/user/<user_id>",methods=['POST'])
def mov_action(direction, velocity, user_id, game_id):
    if(move_by_user(game_id, user_id, direction, velocity)):
        return Response(status=200)
    else:
        return Response(status=404)

@infantry.route("/shoot/<direction>/<figure_id>/<game_id>",methods=['POST'])
def shoot_entity(direction, figure_id, game_id):

    if(shoot(direction, figure_id, game_id)):
        return Response(status=200)
    else:
        return Response(status=404)



    
# Routes here
