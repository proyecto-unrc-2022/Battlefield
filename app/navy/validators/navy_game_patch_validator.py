from marshmallow import Schema, ValidationError, fields, validates_schema


class NavyGamePatchValidator(Schema):

    user2_id = fields.Integer()
    game_id = fields.Integer(required=True)

    @validates_schema
    def validate_game(self, in_data, **kwargs):
        from app.navy.daos.navy_game_dao import navy_game_dao
        from app.navy.utils.navy_game_statuses import WAITING_PLAYERS

        game = navy_game_dao.get_by_id(in_data["game_id"])
        if not (game.status == WAITING_PLAYERS):
            raise ValidationError(
                "Can't join a game with two players", field_name="game_id"
            )

        if game.user1_id == in_data["user2_id"]:
            raise ValidationError("Can't join your own game", field_name="user_id")
