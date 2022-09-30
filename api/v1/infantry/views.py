from api import token_auth

from app import db

from flask import Response

from app.daos.infantry.infantry_dao import add_entity
from . import infantry

@infantry.route("/<entity_id>",methods=['POST'])
def choose_entity(entity_id):
    if (add_entity(entity_id)):
        return Response(status=200)
    else:
        return Response(status=404)
    
        
        


# Routes here
