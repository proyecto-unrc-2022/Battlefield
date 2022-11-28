from flask import url_for
from flask_restx import Namespace, Resource, fields

ship_namespace = Namespace("Ship", path="/api/v1/navy", description="Routes")


ship_types_response_model = ship_namespace.model(
    "ShipTypesResponse",
    {
        "Battleship": fields.Nested(
            ship_namespace.model(
                "ShipTypeModel",
                {
                    "hp": fields.Integer(description="The ship hp"),
                    "missile_type_id": fields.List(
                        fields.Integer, description="The ship missile_type_id"
                    ),
                    "ship_id": fields.Integer(description="The ship id"),
                    "size": fields.Integer(description="The ship size"),
                    "speed": fields.Integer(description="The ship speed"),
                    "visibility": fields.Integer(description="The ship visibility"),
                },
            )
        ),
        "Corvette": fields.Nested(
            ship_namespace.model(
                "ShipTypeModel",
                {
                    "hp": fields.Integer(description="The ship hp"),
                    "missile_type_id": fields.List(
                        fields.Integer, description="The ship missile_type_id"
                    ),
                    "ship_id": fields.Integer(description="The ship id"),
                    "size": fields.Integer(description="The ship size"),
                    "speed": fields.Integer(description="The ship speed"),
                    "visibility": fields.Integer(description="The ship visibility"),
                },
            )
        ),
        "Cruiser": fields.Nested(
            ship_namespace.model(
                "ShipTypeModel",
                {
                    "hp": fields.Integer(description="The ship hp"),
                    "missile_type_id": fields.List(
                        fields.Integer, description="The ship missile_type_id"
                    ),
                    "ship_id": fields.Integer(description="The ship id"),
                    "size": fields.Integer(description="The ship size"),
                    "speed": fields.Integer(description="The ship speed"),
                    "visibility": fields.Integer(description="The ship visibility"),
                },
            )
        ),
        "Destroyer": fields.Nested(
            ship_namespace.model(
                "ShipTypeModel",
                {
                    "hp": fields.Integer(description="The ship hp"),
                    "missile_type_id": fields.List(
                        fields.Integer, description="The ship missile_type_id"
                    ),
                    "ship_id": fields.Integer(description="The ship id"),
                    "size": fields.Integer(description="The ship size"),
                    "speed": fields.Integer(description="The ship speed"),
                    "visibility": fields.Integer(description="The ship visibility"),
                },
            )
        ),
    },
)

"""
{
  "pos_x": 1,
  "pos_y": 4,
  "name": "Destroyer",
  "course": "E",
  "user_id": 2,
  "navy_game_id": 1
}
"""

ship_request_post_model = ship_namespace.model(
    "ShipRequestPost",
    {
        "pos_x": fields.Integer(description="The ship pos_x"),
        "pos_y": fields.Integer(description="The ship pos_y"),
        "name": fields.String(description="The ship name"),
        "course": fields.String(description="The ship course"),
        "navy_game_id": fields.Integer(description="The ship navy_game_id"),
    },
)


@ship_namespace.route("/ships", methods=["POST"])
class Ship(Resource):
    @ship_namespace.response(201, "CREATED")
    @ship_namespace.response(400, "Bad Request")
    @ship_namespace.response(401, "Unauthorized")
    @ship_namespace.response(403, "Forbidden")
    @ship_namespace.response(404, "Not Found")
    @ship_namespace.response(500, "Internal Server Error")
    @ship_namespace.expect(ship_request_post_model)
    def post(self):
        """
        Create a ship
        """
        return url_for("api.v1.new_ship", _external=True)


@ship_namespace.route("/ship_types", methods=["GET"])
class ShipTypes(Resource):
    @ship_namespace.response(200, "Success", ship_types_response_model)
    @ship_namespace.response(400, "Bad Request")
    @ship_namespace.response(401, "Unauthorized")
    @ship_namespace.response(403, "Forbidden")
    @ship_namespace.response(404, "Not Found")
    @ship_namespace.response(500, "Internal Server Error")
    def get(self):
        """
        Get all ship types
        """
        return url_for("api.v1.ship_types", _external=True)
