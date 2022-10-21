from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)
from sqlalchemy import and_, or_

from app import db
from app.models.user import User
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.models.ship import Ship
from app.navy.services.missile_service import missile_service
from app.navy.utils.navy_utils import utils


class ActionRequestValidator(Schema):
    @validates("user_id")
    def validate_user_id(self, user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValidationError("User not found")

    @validates("navy_game_id")
    def validate_navy_game_id(self, navy_game_id):
        from app.navy.models.navy_game import NavyGame

        navy_game = db.session.query(NavyGame).filter_by(id=navy_game_id).first()
        if not navy_game:
            raise ValidationError("Game not found")

    @validates_schema
    def check_move(self, in_data, **kwargs):

        if in_data.get("attack") and in_data.get("move"):
            raise ValidationError("Invalid move")

        if not in_data.get("attack"):
            ship = db.session.query(Ship).filter_by(id=in_data.get("ship_id")).first()

            if ship:
                mov_ship = ship_type_dao.get_by(ship.name)["speed"]
                print(in_data.get("move"))
                if in_data.get("move") < 0:
                    raise ValidationError("The movement is a negative distance")
                if in_data.get("move") > mov_ship:
                    raise ValidationError(
                        "Can't move more than " + str(mov_ship) + " spaces"
                    )

    @validates_schema
    def check_game(self, in_data, **kwargs):
        from app.navy.models.action import Action
        from app.navy.models.navy_game import NavyGame

        user_id = in_data.get("user_id")
        navy_game_id = in_data.get("navy_game_id")
        navy_game_user: NavyGame = (
            db.session.query(NavyGame)
            .filter(
                and_(
                    NavyGame.id == navy_game_id,
                    (or_(NavyGame.user1_id == user_id, NavyGame.user2_id == user_id)),
                )
            )
            .first()
        )

        if not navy_game_user:
            raise ValidationError("Invalid game")

        self.check_ship(in_data, **kwargs)

        actions = (
            db.session.query(Action)
            .filter_by(navy_game_id=navy_game_id, user_id=user_id)
            .all()
        )
        if actions:
            raise ValidationError("No its your turn yet")

    def check_ship(self, in_data, **kwargs):
        ship = db.session.query(Ship).filter_by(id=in_data.get("ship_id")).first()

        if not ship:
            raise ValidationError("Ship not found")

        elif ship.user_id != in_data.get("user_id") or ship.navy_game_id != in_data.get(
            "navy_game_id"
        ):
            raise ValidationError("Invalid ship in game")

    missile_type_id = fields.Integer(
        validate=validate.OneOf(missile_service.MISSILE_TYPES), required=True
    )
    user_id = fields.Integer(required=True)
    navy_game_id = fields.Integer(required=True)
    course = fields.Str(validate=validate.OneOf(utils.DIRECTIONS), required=True)
    ship_id = fields.Int(required=True)
    move = fields.Int(required=True)
    attack = fields.Integer(validate=validate.OneOf([1, 0]), required=True)
