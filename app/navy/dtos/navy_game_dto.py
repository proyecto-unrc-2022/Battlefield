from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.navy.models.navy_game import NavyGame
from app.navy.utils.navy_utils import utils
from app.models.user import UserSchema


class NavyGameDTO(SQLAlchemySchema):
    class Meta:
        model = NavyGame
        include_relationships = True
        load_instances = True

    id = auto_field()
    board_rows = auto_field()
    board_colums = auto_field()
    winner = auto_field()
    round = auto_field()
    turn = auto_field()
    status = auto_field()
    user_1 = Nested(UserSchema)
    user_2 = Nested(UserSchema)

