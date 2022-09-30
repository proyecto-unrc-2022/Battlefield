from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship

from app import db

class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hp = db.Column(db.Integer, unique=True, nullable=False)
    velocidad = db.Column(db.Integer, unique=True, nullable=False)

    

    def __init__(self, hp=None, velocidad=None):
        self.hp = hp
        self.velocidad = velocidad

