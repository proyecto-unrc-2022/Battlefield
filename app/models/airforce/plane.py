from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship

from app import db


class Plane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)



class PlaneSchema(SQLAlchemySchema):
    class Meta:
        model = Plane

    name = auto_field()
    size = auto_field()
    speed = auto_field()
    health = auto_field()
