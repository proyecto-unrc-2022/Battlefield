from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.underwater.under_models import Submarine, Torpedo, UnderGame


class SubmarineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Submarine
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()
    size = auto_field()
    speed = auto_field()
    visibility = auto_field()
    radar_scope = auto_field()
    health = auto_field()
    torpedo_speed = auto_field()
    torpedo_damage = auto_field()
    x_position = auto_field()
    y_position = auto_field()
    direction = auto_field()
    game_id = auto_field()
    player_id = auto_field() 

class TorpedoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Torpedo
        include_relationships = True
        load_instance = True

    id = auto_field()
    speed = auto_field()
    damage = auto_field()
    x_position = auto_field()
    y_position = auto_field()
    direction = auto_field()

    game_id = auto_field()


class UnderGameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UnderGame
        include_relationships = True
        load_instance = True

    id = auto_field()
    host_id = auto_field()
    visitor_id = auto_field()

    submarines = Nested(SubmarineSchema, many=True)
    torpedos = Nested(TorpedoSchema, many=True)
