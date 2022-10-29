from pyexpat import model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship #investigar

from app import db
from app.models.user import User



class Game_Infantry(db.Model):
    __tablename__ = "game_infantry"

    id = db.Column(db.Integer, primary_key=True)
    id_user1 = db.Column(db.Integer, db.ForeignKey(User.id))
    id_user2 = db.Column(db.Integer, db.ForeignKey(User.id))   
    turn = db.Column(db.Integer, nullable=False) 

    #Foreign key
    user_1 = relationship("User", foreign_keys=[id_user1])
    user_2 = relationship("User", foreign_keys=[id_user2])

    def __init__(self, id_user1=None, id_user2=None, turn=1):
        self.id_user1 = id_user1
        self.id_user2 = id_user2 
        self.turn = turn

class Game_Infantry_Schema(SQLAlchemySchema):
    class Meta:
        model= Game_Infantry
        include_relationships = True
        load_instance = True

    id = auto_field()
    id_user1 = auto_field()
    id_user2 = auto_field()
    turn = auto_field()