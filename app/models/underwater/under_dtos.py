from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.underwater.under_models import Submarine, Torpedo, UnderGame


class UnderGameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UnderGame
        include_relationships = True
        load_instance = True

    id = auto_field()
    host_id = auto_field()
    visitor_id = auto_field()


# class SubmarineSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model
