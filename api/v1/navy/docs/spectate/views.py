from flask import url_for
from flask_restx import Namespace, Resource, fields

spectate_namespace = Namespace("Spectate", path="/api/v1/navy", description="Routes")


@spectate_namespace.route("/spectate/<int:navy_game_id>")
class Spectate(Resource):
    @spectate_namespace.doc("Spectate")
    @spectate_namespace.response(200, "Success")
    @spectate_namespace.response(404, "Not Found")
    @spectate_namespace.response(401, "Unauthorized")
    @spectate_namespace.response(403, "Forbidden")
    @spectate_namespace.response(400, "Bad Request")
    @spectate_namespace.response(500, "Internal Server Error")
    def get(self, id):
        """
        Spectate a navy game
        """
        return url_for("api.v1.navy.spectate_navy_game", _external=True)
