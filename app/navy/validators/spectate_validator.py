from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validates_schema,
)
from app import db

class SpectateValidator(Schema):

    @validates_schema
    def check_round(self, in_data, **kwargs):
        from app.navy.models.navy_game import NavyGame
        navy_game = db.session.query(NavyGame).filter_by(id=in_data.get("navy_game_id")).first()
        round = in_data.get("round")
        if not navy_game:
            raise ValidationError("Game doesn't exist.")

        if navy_game.status != "STARTED":
            raise ValidationError("Game hasn't started yet.")
        
        if not navy_game.round - round >= 2 :
            raise ValidationError("Invalid round") 

    round = fields.Integer(required=True)
    navy_game_id = fields.Integer(required=True)
   