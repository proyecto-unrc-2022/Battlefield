from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.user import UserSchema
from app.navy.models.navy_game import NavyGame


class NavyGameDTO(SQLAlchemySchema):
    class Meta:
        model = NavyGame
        include_relationships = True
        load_instances = True

    id = auto_field()
    rows = auto_field()
    cols = auto_field()
    winner = auto_field()
    round = auto_field()
    turn = auto_field()
    status = auto_field()
    user_1 = Nested(UserSchema)
    user_2 = Nested(UserSchema)
