from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.navy.services.ship_service import ship_service
from app.navy.utils.navy_utils import utils


class ShipRequestValidator(Schema):

    name = fields.Str(required=True, validate=validate.OneOf(ship_service.SHIP_NAMES))
    pos_x = fields.Integer(required=True, validate=validate.Range(min=utils.ONE))
    pos_y = fields.Integer(required=True, validate=validate.Range(min=utils.ONE))
    course = fields.Str(required=True, validate=validate.OneOf(utils.DIRECTIONS))
    user_id = fields.Integer()
    navy_game_id = fields.Integer(required=True)

    @validates_schema
    def validate_game(self, in_data, **kwargs):
        from app.navy.daos.navy_game_dao import navy_game_dao
        from app.navy.utils.navy_game_statuses import FINISHED, STARTED, WAITING_PLAYERS

        game = navy_game_dao.get_by_id(in_data.get("navy_game_id"))
        user_id = in_data.get("user_id")

        if not game:
            raise ValidationError("Game doesn't exist.", field_name="navy_game_id")

        if game.user1_id != user_id and game.user2_id != user_id:
            raise ValidationError("Invalid game", field_name="navy_game_id")

        if game.status == FINISHED:
            raise ValidationError(
                "Can't create a ship when the game has already finished",
                field_name="navy_game_id",
            )

        if game.status == STARTED:
            raise ValidationError(
                "Can't create a ship when the game has already started",
                field_name="navy_game_id",
            )

        if game.status == WAITING_PLAYERS:
            raise ValidationError(
                "Can't create a ship when the game has one player",
                field_name="navy_game_id",
            )

    @validates_schema
    def validate_positions(self, in_data, **kwargs):
        from app.navy.daos.navy_game_dao import navy_game_dao

        navy_game_id = in_data.get("navy_game_id")
        game = navy_game_dao.get_by_id(navy_game_id)
        user_id = in_data.get("user_id")

        x = in_data.get("pos_x")
        y = in_data.get("pos_y")

        ship_positions = self.build_completely(
            x, y, in_data.get("course"), self.get_size_by_name(in_data.get("name"))
        )

        if game.user1_id == user_id:
            for x, y in ship_positions:
                if x > game.rows or not (y <= game.cols / 2):
                    raise ValidationError("Ship can't be builded out of range")

        if game.user2_id == user_id:
            for x, y in ship_positions:
                if x > game.rows or not (y > (game.cols / 2) and y <= game.cols):
                    raise ValidationError("Ship can't be builded out of range")

    def build_completely(self, pos_x, pos_y, course, size):
        res = [(pos_x, pos_y)]
        x, y = pos_x, pos_y

        for _ in range(utils.ONE, size):
            if utils.out_of_bounds(x, y):
                raise ValidationError("Ship can't be builded out of range")
            x, y = utils.get_next_position(x, y, utils.INVERSE_COORDS[course])
            res.append((x, y))
        return res

    def get_size_by_name(self, name):
        SHIP_SIZES = [3, 3, 4, 2]
        i = ship_service.SHIP_NAMES.index(name)
        return SHIP_SIZES[i]
