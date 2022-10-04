from ast import Raise

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_load,
    validate,
    validates,
    validates_schema,
)

from app.models.navy.dynamic_game import Game
from app.models.navy.dynamic_ship import DynamicShip
from app.models.user import User
from app.navy.navy_constants import DIRECTIONS, MISSILES_TYPES, SHIP_TYPES
from app.navy.navy_utils import get_move_ship_


class ActionGameRequest(Schema):
    @validates_schema
    def check_move(self, in_data, **kwargs):

        if in_data.get("attack") == 1 and in_data.get("move") != 0:
            raise ValidationError("Invalid move")

        if in_data.get("attack") == 0:
            mov_ship = get_move_ship_(in_data.get("ship_type"))

            if in_data.get("move") > mov_ship:
                raise ValidationError(
                    "Can't move more than " + str(mov_ship) + " spaces"
                )

    @validates_schema
    def check_ship(self, in_data, **kwargs):
        ship = DynamicShip.query.filter_by(id=in_data.get("id_ship")).first()
        if ship.id_game != in_data.get("id_game"):
            raise ValidationError("The game you tried to access is invalid")
        elif ship.id_user != in_data.get("id_user"):
            raise ValidationError("Invalid user")

    @validates("id_user")
    def validate_id_user(self, id_user):
        user = User.query.filter_by(id=id_user).first()
        if not user:
            raise ValidationError("User not found")

    @validates("id_game")
    def validate_id_game(self, id_game):
        game = Game.query.filter_by(id=id_game).first()
        if not game:
            raise ValidationError("Game not found")
        """ elif game.user_id != in_data.get("id_user"):
            print("Entre")
            raise ValidationError("Estas accediendo a un juego que no es") """

    id_missile = fields.Integer(validate=validate.OneOf(MISSILES_TYPES), required=True)
    id_user = fields.Integer(required=True)
    id_game = fields.Integer(required=True)
    dir = fields.Str(validate=validate.OneOf(DIRECTIONS), required=True)
    id_ship = fields.Int(required=True)
    move = fields.Int(required=True)
    ship_type = fields.Int(validate=validate.OneOf(SHIP_TYPES), required=True)
    attack = fields.Integer(validate=validate.OneOf([0, 1]), required=True)
