from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.navy.dtos.missile_dto import MissileDTO
from app.navy.dtos.ship_dto import ShipDTO
from app.navy.models.navy_game import NavyGame
from app.navy.utils.navy_utils import utils


class NavyGameDTO(SQLAlchemySchema):
    class Meta:
        model = NavyGame
        include_relationships = True
        load_instances = True

    id = auto_field()
    user1_id = auto_field()
    user2_id = auto_field()
    board_rows = auto_field()
    board_colums = auto_field()
    winner = auto_field()
    round = auto_field()
    turn = auto_field()
    ready_to_play = fields.Method("is_ready_to_play")
    ships = Nested(ShipDTO, many=True)
    missiles = Nested(MissileDTO, many=True)

    def is_ready_to_play(self, obj):
        if obj.ready_to_play:
            return True
        return len(set([ship.user_id for ship in obj.ships])) == utils.CANT_PLAYERS
