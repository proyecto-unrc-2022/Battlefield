from pyexpat import model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship #investigar

from app import db
from app.models.user import User
from app.models.infantry.game_Infantry import Game_Infantry


class Projectile_infantry(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey(Game_Infantry.id))
    pos_x = db.Column(db.Integer, nullable=False)
    pos_y = db.Column(db.Integer, nullable=False)
    velocidad = db.Column(db.Integer, nullable=False)
    daño = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    
    
    #Foreign key
    game = relationship("Game_Infantry", foreign_keys=[id_game])

    def __init__(self, id_game=None, pos_x=None, pos_y=None, velocidad=None, daño=None, direccion=None, type=None):
        self.id_game = id_game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocidad = velocidad
        self.daño = daño
        self.direccion = direccion
        self.type = type


class Projectile_Infantry_Schema(SQLAlchemySchema):
    class Meta:
        model= Projectile_infantry
        include_relationships = True
        load_instance = True

    id_game = auto_field()
    pos_x = auto_field()
    pos_y = auto_field()
    velocidad = auto_field()
    daño = auto_field()
    direccion = auto_field()
    type = auto_field()
