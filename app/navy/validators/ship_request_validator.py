from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)

from app import db
from app.models.user import User
from app.navy.models.navy_game import NavyGame
from app.navy.services.ship_service import ship_service
from app.navy.utils.navy_utils import utils


class ShipRequestValidator(Schema):

    name = fields.Str(required=True, validate=validate.OneOf(ship_service.SHIP_NAMES))

    # TODO: Validar rows y cols desde game
    pos_x = fields.Integer(
        required=True, validate=validate.Range(min=utils.ONE, max=utils.ROWS)
    )
    pos_y = fields.Integer(
        required=True, validate=validate.Range(min=utils.ONE, max=utils.COLS)
    )
    course = fields.Str(required=True, validate=validate.OneOf(utils.DIRECTIONS))
    user_id = fields.Integer(required=True)
    navy_game_id = fields.Integer(required=True)

    @validates("user_id")
    def validate_user(self, user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValidationError("User doesn't exist.")

    @validates("navy_game_id")
    def validate_navy_game(self, navy_game_id):
        game = db.session.query(NavyGame).filter_by(id=navy_game_id).first()
        if not game:
            raise ValidationError("Game doesn't exist.")

    @validates_schema
    def check_positions(self, in_data, **kwargs):
        game = (
            db.session.query(NavyGame).filter_by(id=in_data.get("navy_game_id")).first()
        )
        user = db.session.query(User).filter_by(id=in_data.get("user_id")).first()
        y = in_data.get("pos_y")

        if game and user:
            if game.user1_id == user.id and (utils.ONE > y or utils.COLS / 2 < y):
                raise ValidationError("Y coord of user 1, must be between 1 or 10")

            if game.user2_id == user.id and (utils.COLS / 2 >= y or utils.COLS < y):
                raise ValidationError("Y coord of user 2, must be between 11 and 20")
        else:
            raise ValidationError("User or Game don't exist.")
