from flask import url_for
from flask_restx import Namespace, Resource, fields

navy_namespace = Namespace("Navy Game", path="/api/v1/navy", description="Routes")


navy_games_model = navy_namespace.model(
    "NavyGame",
    {
        "id": fields.Integer(required=True, description="The game id"),
        "cols": fields.Integer(required=True, description="The game cols"),
        "rows": fields.Integer(required=True, description="The game rows"),
        "round": fields.Integer(required=True, description="The game round"),
        "status": fields.String(required=True, description="The game status"),
        "turn": fields.String(required=True, description="The game turn"),
        "user1": fields.Integer(required=True, description="The info of user1"),
        "user2": fields.Integer(required=True, description="The info of user2"),
        "winner": fields.Integer(required=True, description="The winner of the game"),
    },
)


navy_user_get_model = navy_namespace.model(
    "NavyGame",
    {
        "cols": fields.Integer(description="The game cols"),
        "id": fields.Integer(description="The game id"),
        "round": fields.Integer(description="The game round"),
        "rows": fields.Integer(description="The game rows"),
        "ship": fields.Nested(
            navy_namespace.model(
                "Ship",
                {
                    "course": fields.String(description="The ship course"),
                    "hp": fields.Integer(description="The ship hp"),
                    "id": fields.Integer(description="The ship id"),
                    "name": fields.String(description="The ship name"),
                    "pos_x": fields.Integer(description="The ship pos_x"),
                    "pos_y": fields.Integer(description="The ship pos_y"),
                    "size": fields.Integer(description="The ship size"),
                    "speed": fields.Integer(description="The ship speed"),
                },
            )
        ),
        "sight_range": fields.Nested(navy_namespace.model("SightRange", {
            "missiles" : fields.List(fields.Nested(navy_namespace.model("Missile", {}))),
            "ships" : fields.List(fields.Nested(navy_namespace.model("Ship", {}))),
        })),
        "status": fields.String(description="The game status"),
        "turn": fields.Integer(description="The game turn"),
        "user_1": fields.Nested(navy_namespace.model("User", {})),
        "user_2": fields.Nested(navy_namespace.model("User", {})),
        "winner": fields.Integer(description="The winner of the game"),
    },
)


navy_get_model = navy_namespace.model(
    "NavyUserGame",
    {
        "cols": fields.Integer(description="The game cols"),
        "id": fields.Integer(description="The game id"),
        "round": fields.Integer(description="The game round"),
        "rows": fields.Integer(description="The game rows"),
        "status": fields.String(description="The game status"),
        "turn": fields.Integer(description="The game turn"),
        "user_1": fields.Nested(navy_namespace.model("User", {
            "email": fields.String(description="The user email"),
            "id": fields.Integer(description="The user id"),
            "username": fields.String(description="The user username"),
        })),
        "user_2": fields.Nested(navy_namespace.model("User", {
            "email": fields.String(description="The user email"),
            "id": fields.Integer(description="The user id"),
            "username": fields.String(description="The user username"),
        })),
        "winner": fields.Integer(description="The winner of the game"),
    },
)




@navy_namespace.route("/navy_games")
class NavyGames(Resource):
    @navy_namespace.doc("get all navy games")
    @navy_namespace.response(200, "Success", model=navy_get_model)
    @navy_namespace.response(400, "Validation Error")
    @navy_namespace.response(401, "Unauthorized")
    def get(self, **kwargs):
        """
        Get all games
        """
        return url_for("api.v1.navy_games", _external=True)

    @navy_namespace.doc("create a new navy game")
    @navy_namespace.response(201, "Creation game success", model=navy_get_model)
    @navy_namespace.response(400, "Validation Error")
    @navy_namespace.response(401, "Unauthorized")
    def post(self, **kwargs):
        """
        Create a new game
        """
        return url_for("api.v1.navy_games", _external=True)


@navy_namespace.route("/navy_games/<int:id>")
class NavyGame(Resource):
    @navy_namespace.doc("get a navy game")
    @navy_namespace.response(200, "Success", model=navy_user_get_model)
    def get(self, id):
        """
        Get a navy game
        """
        return url_for("api.v1.navy_games", _external=True)



    @navy_namespace.doc("update a navy game")
    @navy_namespace.response(200, "Success", model=navy_get_model)
    @navy_namespace.response(400, "Validation Error")
    @navy_namespace.response(401, "Unauthorized")
    @navy_namespace.response(404, "Not Found")
    @navy_namespace.response(500, "Internal Server Error")
    def patch(self, id):
        """
        Join a navy game
        """
        return url_for("api.v1.navy_games", _external=True)

    @navy_namespace.doc("delete a navy game")
    @navy_namespace.response(204, "Success")
    @navy_namespace.response(400, "Validation Error")
    @navy_namespace.response(401, "Unauthorized")
    def delete(self, id):
        """
        Delete a  navy game
        """
        return url_for("api.v1.navy_games", _external=True)
