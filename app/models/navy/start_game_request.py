from marshmallow import fields, Schema, validates, ValidationError, validate
from app.models.navy.dynamic_game import Game
from app.models.user import User
from app.navy.navy_constants import DIRECTIONS, ROWS, COLS, SHIP_TYPES

class StartGameRequest(Schema):
  game_id = fields.Integer(required=True)
  id_user = fields.Integer(required=True)
  direction = fields.Str(validate=validate.OneOf(DIRECTIONS), required=True)
  pos_x = fields.Int(validate=validate.Range(min=1, max=ROWS), required=True) 
  pos_y = fields.Int(validate=validate.Range(min=1, max=COLS), required=True)
  ship_type = fields.Int(validate=validate.OneOf(SHIP_TYPES), required=True)

  @validates("game_id")
  def validate_game_existence(self, value):
    if not bool(Game.query.filter_by(id=value).first()):
      raise ValidationError("Game doesn't exist.")
    

  @validates("id_user")
  def validate_user_existence(self, value):
    if not bool(User.query.filter_by(id=value).first()):
      raise ValidationError("User doesn't exist.")