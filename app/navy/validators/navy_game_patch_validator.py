from marshmallow import Schema, ValidationError, fields, validates

from app.models.user import User


class NavyGamePatchValidator(Schema):
    user2_id = fields.Integer(required=True)

    @validates("user2_id")
    def validate_game_existence(self, value):
        if not bool(User.query.filter_by(id=value).first()):
            raise ValidationError("User doesn't exist.")
