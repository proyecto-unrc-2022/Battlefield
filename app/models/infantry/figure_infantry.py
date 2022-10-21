#from turtle import back
from pyexpat import model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship #investigar

from app import db
from app.models.user import User
from app.models.infantry.game_Infantry import Game_Infantry


class Figure_infantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(User.id))
    id_game = db.Column(db.Integer, db.ForeignKey(Game_Infantry.id))
    hp = db.Column(db.Integer, nullable=False)
    velocidad = db.Column(db.Integer, nullable=False)
    tamaño = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.Integer, nullable=False)
    pos_x = db.Column(db.Integer, nullable=False)
    pos_y = db.Column(db.Integer, nullable=False)
    figure_type = db.Column(db.Integer, nullable=False)
    
    #Foreign key
    game = relationship("Game_Infantry", foreign_keys=[id_game])
    user = relationship("User", foreign_keys=[id_user])
    
    def __init__(self, id_user=None, id_game=None, hp=None, velocidad=None, tamaño=None, direccion=None, pos_x=None, pos_y=None, type=None):
        self.id_user = id_user #game.user_1 preguntar como pasar  
        self.id_game = id_game #game preguntar como pasar 
        self.hp = hp
        self.velocidad = velocidad
        self.tamaño = tamaño
        self.direccion = direccion
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.figure_type = type

class Figure_Infantry_Schema(SQLAlchemySchema):
    class Meta:
        model= Figure_infantry
        include_relationships = True
        load_instance = True

    id_user = auto_field()
    id_game = auto_field()
    hp = auto_field()
    velocidad = auto_field()
    tamaño = auto_field()
    direccion = auto_field()
    pos_x = auto_field()
    pos_y = auto_field()
    figure_type = auto_field()