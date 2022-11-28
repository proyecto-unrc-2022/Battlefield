from flask import url_for
from flask_restx import Namespace, Resource, fields

navy_actions_namespace = Namespace("Action", path="/api/v1/navy", description="Routes")


navy_action_post_model = navy_actions_namespace.model(
    "NavyActionPost",
    {
        "missile_type_id": fields.Integer(required=True),
        "navy_game_id": fields.Integer(required=True),
        "course": fields.String(required=True),
        "ship_id": fields.Integer(required=True),
        "move": fields.Integer(required=True),
        "attack": fields.Integer(required=True),
        "round": fields.Integer(required=True),
    },
)


@navy_actions_namespace.route("/actions")
class NavyAction(Resource):
    @navy_actions_namespace.doc(
        responses={
            201: "OK",
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    @navy_actions_namespace.expect(navy_action_post_model)
    def post(self):
        """
        Create a new action
        """
        return url_for("api.v1.navy_actions", _external=True)
