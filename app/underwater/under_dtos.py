from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

# from app.underwater.models.under_models import Submarine, Torpedo, UnderGame
from app.underwater.models.submarine import Submarine
from app.underwater.models.submerged_object import SubmergedObject
from app.underwater.models.torpedo import Torpedo
from app.underwater.models.under_game import UnderGame

# class SmartNested(Nested):
#     def serialize(self,attr,obj,accessor=None):
#         if type(attr) is Submarine:
#             return super(SubmarineSchema, many=False)
#         else:
#             return super(TorpedoSchema, many=False)


class SubmergedObjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SubmergedObject
        include_relationships = True
        load_instance = True


class SubmarineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Submarine
        include_relationships = True
        load_instance = True


class TorpedoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Torpedo
        include_relationships = True
        load_instance = True


class UnderGameSchema(SQLAlchemySchema):
    class Meta:
        model = UnderGame
        include_relationships = True
        load_instance = True

    id = auto_field()
    host_id = auto_field()
    visitor_id = auto_field()

    # submarines = Nested(SubmarineSchema, many=True)
    # torpedos = Nested(TorpedoSchema, many=True)

    submerged_objects = Nested(SubmergedObjectSchema, many=True)


game_dto = UnderGameSchema()
