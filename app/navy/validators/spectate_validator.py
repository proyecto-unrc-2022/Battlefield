from marshmallow import Schema, ValidationError, fields, validates_schema


class SpectateValidator(Schema):
    @validates_schema
    def check_round(self, in_data, **kwargs):

        from app.navy.daos.navy_game_dao import navy_game_dao
        from app.navy.utils.navy_game_statuses import FINISHED, STARTED

        game = navy_game_dao.get_by_id(in_data.get("navy_game_id"))
        round = in_data.get("round")

        if not game:
            raise ValidationError("Game doesn't exist.")

        if game.round < 3:
            raise ValidationError("Game unvailable for spectate.")

        if game.status != STARTED and game.status != FINISHED:
            raise ValidationError("Game hasn't started yet.")

        if round != 0 and not game.round - round >= 1 and game.status != FINISHED:
            raise ValidationError("Invalid round")

    round = fields.Integer(required=True)
    navy_game_id = fields.Integer(required=True)
