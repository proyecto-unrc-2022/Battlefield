from flask import Blueprint
from flask_restx import Api
from api.v1.navy.docs.navy_games.views import navy_namespace
from api.v1.navy.docs.actions.views import navy_actions_namespace
from api.v1.navy.docs.ships.views import ship_namespace
from api.v1.navy.docs.missiles.views import missile_namespace
navy_doc = Blueprint("documented_navy_api", __name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
api = Api(app=navy_doc,
    title="Navy API",
    license="FREE",
    license_url="http//www.google.com",
    version="1.0",
    description="Documentation for the Navy API - Final Project",
    authorizations=authorizations,
    security='Bearer Auth',
    default_mediatype="application/json",

)



    
    

api.add_namespace(missile_namespace)
api.add_namespace(ship_namespace)
api.add_namespace(navy_actions_namespace)
api.add_namespace(navy_namespace)