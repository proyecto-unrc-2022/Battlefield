from marshmallow import fields, Schema, validates, ValidationError
from app.navy.models.navy_game import NavyGame

class NavyGameRequestValidator(Schema):
  user1_id = fields.Integer(required=True)

  @validates("user1_id")
  def validate_game_existence(self, value):
    if not bool(NavyGame.query.filter_by(id=value).first()):
      raise ValidationError("Game doesn't exist.")