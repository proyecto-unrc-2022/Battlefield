from app.navy.models.missile import Missile
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, fields

class MissileSchema(SQLAlchemySchema):
    class Meta:
        model = Missile
        include_relationships = False
        load_instance = True

    id = auto_field()
    navy_game_id = auto_field()
    ship_id = auto_field()
    speed = auto_field()
    damage = auto_field()
    course = auto_field()
    pos_x = auto_field()
    pos_y = auto_field()
    order = auto_field()
    
