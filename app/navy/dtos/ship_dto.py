from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.navy.models.ship import Ship


class ShipDTO(SQLAlchemySchema):
    class Meta:
        model = Ship
        include_relationships = False
        load_instance = True

    id = auto_field()
    user_id = auto_field()
    name = auto_field()
    hp = auto_field()
    size = auto_field()
    speed = auto_field()
    pos_x = auto_field()
    pos_y = auto_field()
    course = auto_field()
