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
    course = db.Column(db.Integer)
    coor_x = db.Column(db.Integer)
    coor_y = db.Column(db.Integer)



class PlaneSchema(SQLAlchemySchema):
    class Meta:
        model = Plane

    name = auto_field()
    size = auto_field()
    speed = auto_field()
    health = auto_field()
    course = auto_field()
    coor_x = auto_field()
    coor_y = auto_field()


class Projectile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speed = db.Column(db.Integer, nullable=False)
    damage = db.Column(db.Integer, nullable=False)


class ProjectileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Projectile

    speed = auto_field()
    damage = auto_field()
    
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
        
        damage_1 = auto_field() # Mas cercano
        damage_2 = auto_field() # Medio
        damage_3 = auto_field() # Mas lejano
        x1 = auto_field()
        y1 = auto_field()
        course = auto_field()

