from flask import Blueprint

from api.v1.navy import navy as navy_blueprint
from api.v1.navy.docs.actions.views import navy_actions_namespace
from api.v1.navy.docs.missiles.views import missile_namespace
from api.v1.navy.docs.navy_games.views import navy_namespace
from api.v1.navy.docs.ships.views import ship_namespace
from api.v1.navy.docs.spectate.views import spectate_namespace
from app import api

navy_doc = Blueprint("documented_navy_api", __name__)
authorizations = {
    "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"},
}

api.title = "Navy API"
api.license = "FREE"
api.license_url = "http//www.google.com"
api.version = "1.0"
api.description = "Documentation for the Navy API - Final Project"
api.authorizations = authorizations
api.security = "Bearer Auth"
api.default_mediatype = "application/json"
api._doc = "/api/v1/navy"


api.add_namespace(missile_namespace)
api.add_namespace(ship_namespace)
api.add_namespace(navy_actions_namespace)
api.add_namespace(navy_namespace)
api.add_namespace(spectate_namespace)
