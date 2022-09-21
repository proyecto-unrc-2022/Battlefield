from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship

from app import db
from app.models.user import User


class AirForceGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_a_id = db.Column(db.Integer, db.ForeignKey(User.id))
    player_b_id = db.Column(db.Integer, db.ForeignKey(User.id))


class Plane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    direct_of_plane = db.Column(db.String(5), nullable=False)
    coor_x = db.Column(db.Integer, nullable=False)
    coor_y = db.Column(db.Integer, nullable=False)


class PlaneSchema(SQLAlchemySchema):
    class Meta:
        model = Plane

    name = auto_field()
    size = auto_field()
    speed = auto_field()
    health = auto_field()
    direct_of_plane = auto_field()
    coor_x = auto_field()
    coor_y = auto_field()
