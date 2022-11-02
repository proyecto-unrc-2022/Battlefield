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

    pos_x = fields.Integer(required=True, validate=validate.Range(min=utils.ONE))
    pos_y = fields.Integer(required=True, validate=validate.Range(min=utils.ONE))
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

        x = in_data.get("pos_x")
        y = in_data.get("pos_y")

        if game and user:
            ship_positions = self.build_completely(
                x, y, in_data.get("course"), self.get_size_by_name(in_data.get("name"))
            )
            if game.user1_id == user.id:
                for x, y in ship_positions:
                    if utils.out_of_bounds(x, y) or (
                        utils.ONE > y or game.board_colums / 2 <= y
                    ):
                        raise ValidationError("Ship can't be builded out of range")

            if game.user2_id == user.id:
                for x, y in ship_positions:
                    if utils.out_of_bounds(x, y) or (
                        utils.COLS / 2 >= y or game.board_colums <= y
                    ):
                        raise ValidationError("Ship can't be builded out of range")

    @validates_schema
    def create_when_game_has_ended(self, in_data, **kwargs):
        game = (
            db.session.query(NavyGame).filter_by(id=in_data.get("navy_game_id")).first()
        )
        if game.winner:
            raise ValidationError(
                "Can't create a ship when the game has already finished"
            )

    @validates_schema
    def create_when_game_has_started(self, in_data, **kwargs):
        from app.navy.models.action import Action

        actions = (
            db.session.query(Action).filter_by(id=in_data.get("navy_game_id")).all()
        )

        if actions:
            raise ValidationError(
                "Can't create a ship when the game has already started"
            )

    def build_completely(self, pos_x, pos_y, course, size):
        res = [(pos_x, pos_y)]
        x, y = pos_x, pos_y
        for _ in range(utils.ONE, size):
            x, y = utils.get_next_position(x, y, utils.INVERSE_COORDS[course])
            res.append((x, y))
        return res

    def get_size_by_name(self, name):
        i = ship_service.SHIP_NAMES.index(name)
        return ship_service.SHIP_SIZES[i]
