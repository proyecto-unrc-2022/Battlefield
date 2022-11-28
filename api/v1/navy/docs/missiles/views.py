from flask import url_for
from flask_restx import Namespace, Resource, fields

missile_namespace = Namespace("Missile", path="/api/v1/navy", description="Routes")

missile_types_response_model = missile_namespace.model(
    "MissileTypesResponse",
    {
        "1": fields.Nested(
            missile_namespace.model(
                "MissileTypeModel",
                {
                    "damage": fields.Integer(description="The missile damage"),
                    "speed": fields.Integer(description="The missile speed"),
                },
            )
        ),
        "2": fields.Nested(
            missile_namespace.model(
                "MissileTypeModel",
                {
                    "damage": fields.Integer(description="The missile damage"),
                    "speed": fields.Integer(description="The missile speed"),
                },
            )
        ),
        "3": fields.Nested(
            missile_namespace.model(
                "MissileTypeModel",
                {
                    "damage": fields.Integer(description="The missile damage"),
                    "speed": fields.Integer(description="The missile speed"),
                },
            )
        ),
        "4": fields.Nested(
            missile_namespace.model(
                "MissileTypeModel",
                {
                    "damage": fields.Integer(description="The missile damage"),
                    "speed": fields.Integer(description="The missile speed"),
                },
            )
        ),
    },
)


@missile_namespace.route("/missile_types", methods=["GET"])
class MissileType(Resource):
    @missile_namespace.response(200, "Success", missile_types_response_model)
    @missile_namespace.response(400, "Bad Request")
    @missile_namespace.response(401, "Unauthorized")
    @missile_namespace.response(403, "Forbidden")
    @missile_namespace.response(404, "Not Found")
    @missile_namespace.response(500, "Internal Server Error")
    def get(self):
        """
        Get all missile types
        """
        return url_for("api.v1.missile_types", _external=True)
