from marshmallow import Schema, ValidationError, fields, validates_schema


class DeleteGameValidator(Schema):

    game_id = fields.Integer(required=True)
    user_id = fields.Integer()

    @validates_schema
    def validate_game(self, in_data, **kwargs):
        from app.navy.daos.navy_game_dao import navy_game_dao
        from app.navy.utils.navy_game_statuses import WAITING_PLAYERS

        game = navy_game_dao.get_by_id(in_data["game_id"])
        if not game:
            raise ValidationError("Game doesn't exist.", field_name="game_id")

        if not (game.status == WAITING_PLAYERS):
            raise ValidationError(
                "Can't delete a game with players.", field_name="game_id"
            )

        if game.user1_id != in_data.get("user_id"):
            raise ValidationError(
                "User is not the host of the game.", field_name="user_id"
            )
