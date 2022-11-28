from marshmallow import Schema, ValidationError, fields, validates_schema


class NavyGameGetValidator(Schema):
    navy_game_id = fields.Integer(required=True)
    user_id = fields.Integer()

    @validates_schema
    def validate_game(self, in_data, **kwargs):
        from app.navy.daos.navy_game_dao import navy_game_dao

        game = navy_game_dao.get_by_id(in_data["navy_game_id"])
        if not game:
            raise ValidationError("Game not found", field_name="navy_game_id")

        if (game.user1_id != in_data["user_id"]) and (
            game.user2_id != in_data["user_id"]
        ):
            raise ValidationError("User not in game", field_name="user_id")
