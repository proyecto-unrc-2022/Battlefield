from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validates_schema,
)

from app.models.user import User

class DeleteGameValidator(Schema):
    game_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    @validates_schema
    def validate_game(self, in_data, **kwargs):
        from app.navy.services.navy_game_service import navy_game_service

        game = navy_game_service.get_by_id(in_data['game_id'])
        if not game:
            raise ValidationError("Game doesn't exist.")

        if game.user1_id and game.user2_id:
            raise ValidationError("Can't delete a game with players.")
        
        if game.user1_id != in_data.get("user_id"):
            raise ValidationError("User is not the host of the game.")