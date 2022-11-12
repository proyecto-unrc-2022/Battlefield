from marshmallow import Schema, ValidationError, fields, validates

from app.models.user import User


class NavyGamePatchValidator(Schema):
    user2_id = fields.Integer(required=True)
    game_id = fields.Integer(required=True)

    @validates("user2_id")
    def validate_user_existence(self, value):
        if not bool(User.query.filter_by(id=value).first()):
            raise ValidationError("User doesn't exist.")
    
    @validates("game_id")
    def validate_game(self, value):
        from app.navy.services.navy_game_service import navy_game_service
        game = navy_game_service.get_by_id(value)
        if bool(game.user1_id) and bool(game.user2_id):
            raise ValidationError("Can't join a game with two players")
