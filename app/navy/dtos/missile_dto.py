from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, fields

from app.navy.models.missile import Missile


class MissileDTO(SQLAlchemySchema):
    class Meta:
        model = Missile
        include_relationships = False
        load_instance = True

    course = auto_field()
    pos_x = auto_field()
    pos_y = auto_field()
