from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship

from app import db


class Plane(db.Model):
    __tablename__ = "plane"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    course = db.Column(db.Integer, nullable=False)  # 1 north, 2 east, 3 south, 4 west
    coor_x = db.Column(db.Integer, nullable=False)
    coor_y = db.Column(db.Integer, nullable=False)

    projectile = relationship("Projectile")


class Projectile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speed = db.Column(db.Integer, nullable=False)
    damage = db.Column(db.Integer, nullable=False)
    plane_id = db.Column(db.Integer, db.ForeignKey("plane.id"))

    # plane = relationship("Plane", back_populates="projectile")


class ProjectileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Projectile
        include_relationship = True
        load_instance = True

    speed = auto_field()
    damage = auto_field()


class PlaneSchema(SQLAlchemySchema):
    class Meta:
        model = Plane
        include_relationship = True
        load_instance = True

    name = auto_field()
    size = auto_field()
    speed = auto_field()
    health = auto_field()
    course = auto_field()
    coor_x = auto_field()
    coor_y = auto_field()
