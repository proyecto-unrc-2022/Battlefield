from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship

from app import db


class Plane(db.Model):
    __tablename__ = "plane"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    cant_projecile = db.Column(db.Integer, nullable=False)

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
    cant_projecile = auto_field()


class Machine_gun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    damage_1 = db.Column(db.Integer, nullable=False)
    damage_2 = db.Column(db.Integer, nullable=False)
    damage_3 = db.Column(db.Integer, nullable=False)
    x1 = db.Column(db.Integer)
    y1 = db.Column(db.Integer)
    course = db.Column(db.Integer)


class Machine_gunSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Machine_gun

        damage_1 = auto_field()  # Mas cercano
        damage_2 = auto_field()  # Medio
        damage_3 = auto_field()  # Mas lejano
        x1 = auto_field()
        y1 = auto_field()
        course = auto_field()
