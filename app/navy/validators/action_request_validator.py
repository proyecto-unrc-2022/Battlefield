from app import db
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)

from app.navy.models.ship import Ship
from app.models.user import User
from app.navy.navy_constants import DIRECTIONS,  SHIP_TYPES
from app.navy.utils.navy_utils import TRUE,FALSE
from app.navy.services.missile_service import MissileService
from app.navy.daos.ship_type_dao import ship_type_dao


class ActionRequestValidator(Schema):
    @validates_schema
    def check_move(self, in_data, **kwargs):

        if in_data.get("attack") == TRUE and in_data.get("move") != FALSE:
            raise ValidationError("Invalid move")

        if in_data.get("attack") == FALSE:
            ship = db.session.execute(db.select(Ship).filter_by(id=in_data.get("ship_id"))).one()
            
            mov_ship = ship_type_dao.get_by(ship.name)['speed']

            if in_data.get("move") > mov_ship:
                raise ValidationError(
                    "Can't move more than " + str(mov_ship) + " spaces"
                )

    @validates_schema
    def check_ship(self, in_data, **kwargs):
        ship = db.session.execute(db.select(Ship).filter_by(id=in_data.get("ship_id"))).one()

        if ship.navy_game_id != in_data.get("navy_game_id"):
            raise ValidationError("The game you tried to access is invalid")
        elif ship.user_id != in_data.get("user_id"):
            raise ValidationError("Invalid user")

    @validates("user_id")
    def validate_user_id(self, user_id):
        user = db.session.execute(db.select(User).filter_by(id=user_id)).one()
        if not user:
            raise ValidationError("User not found")

    @validates("navy_game_id")
    def validate_navy_game_id(self, navy_game_id):
        from app.navy.models.navy_game import NavyGame
        game = db.session.execute(db.select(NavyGame).filter_by(id=navy_game_id)).one()
        if not game:
            raise ValidationError("Game not found")
      

    missile_type_id = fields.Integer(validate=validate.OneOf(MissileService.MISSILE_TYPES), required=True)
    user_id = fields.Integer(required=True)
    navy_game_id = fields.Integer(required=True)
    course = fields.Str(validate=validate.OneOf(DIRECTIONS), required=True)
    ship_id = fields.Int(required=True)
    move = fields.Int(required=True)
    ship_type = fields.Int(validate=validate.OneOf(SHIP_TYPES), required=True)
    attack = fields.Integer(validate=validate.OneOf([TRUE, FALSE]), required=True)
