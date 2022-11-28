from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.navy.models.missile import Missile


class MissileDTO(SQLAlchemySchema):
    class Meta:
        model = Missile
        include_relationships = False
        load_instance = True

    id = auto_field()
    course = auto_field()
    pos_x = auto_field()
    pos_y = auto_field()
    speed = auto_field()
    damage = auto_field()
