from api import token_auth

from app import db

from flask import Response

from app.daos.infantry.infantry_dao import add_entity
from app.models.infantry.entity import Entity
from app.daos.infantry.entity_dao import create_game
from app.daos.infantry.entity_dao import ready

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

@infantry.route("/<entity_id>",methods=['POST'])
def choose_entity(entity_id):
    if (add_entity(entity_id)):
        return Response(status=200)
    else:
        return Response(status=404)


    
# Routes here
