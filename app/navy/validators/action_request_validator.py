from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.navy.utils.navy_utils import utils


class ActionRequestValidator(Schema):

    user_id = fields.Integer()
    navy_game_id = fields.Integer(required=True)
    course = fields.Str(validate=validate.OneOf(utils.DIRECTIONS), required=True)
    ship_id = fields.Int(required=True)
    move = fields.Int(required=True)
    attack = fields.Integer(
        validate=validate.OneOf([utils.ONE, utils.ZERO]), required=True
    )
    round = fields.Integer(required=True)
    missile_type_id = fields.Integer(
        validate=validate.OneOf(utils.MISSILE_TYPES), required=True
    )

    @validates_schema
    def validate_game(self, in_data, **kwargs):

        from app.navy.daos.navy_game_dao import navy_game_dao
        from app.navy.utils.navy_game_statuses import FINISHED, STARTED

        game = navy_game_dao.get_by_id(in_data.get("navy_game_id"))

        user_id = in_data.get("user_id")
        round = in_data.get("round")

        if not game:
            raise ValidationError("Game not found", field_name="navy_game_id")

        if game.user1_id != user_id and game.user2_id != user_id:
            raise ValidationError("Invalid game", field_name="navy_game_id")

        if game.status == FINISHED:
            raise ValidationError("Game finished", field_name="navy_game_id")

        if not (game.status == STARTED):
            raise ValidationError("Game not started yet", field_name="navy_game_id")

        if game.round != round:
            raise ValidationError("Wrong round", field_name="round")

        self.validate_move(in_data, **kwargs)

    def validate_move(self, in_data, **kwargs):
        from app.navy.daos.ship_dao import ship_dao
        from app.navy.daos.ship_type_dao import ship_type_dao

        if in_data.get("attack") and in_data.get("move"):
            raise ValidationError("Invalid action")

        if not in_data.get("attack"):
            self.validate_ship(in_data, **kwargs)
            ship = ship_dao.get_by_id(in_data.get("ship_id"))
            mov_ship = ship_type_dao.get_by(ship.name)["speed"]

            if in_data.get("move") < 0:
                raise ValidationError(
                    "The move is a negative distance", field_name="move"
                )

            if in_data.get("move") > mov_ship:
                raise ValidationError(
                    "Can't move more than " + str(mov_ship) + " spaces",
                    field_name="move",
                )

    @validates_schema
    def validate_action(self, in_data, **kwargs):
        from app.navy.daos.action_dao import action_dao

        user_id = in_data.get("user_id")
        navy_game_id = in_data.get("navy_game_id")
        round = in_data.get("round")

        action = action_dao.get_by_user_round(
            navy_game_id=navy_game_id, round=round, user_id=user_id
        )

        if action:
            raise ValidationError("It's not your turn yet")

    def validate_ship(self, in_data, **kwargs):

        from app.navy.daos.ship_dao import ship_dao

        ship = ship_dao.get_by_id(in_data.get("ship_id"))

        if not ship:
            raise ValidationError("Ship not found", field_name="ship_id")

        if ship.user_id != in_data.get("user_id") or ship.navy_game_id != in_data.get(
            "navy_game_id"
        ):
            raise ValidationError("Invalid ship in game", field_name="ship_id")
