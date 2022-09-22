from dataclasses import field
import json
from sqlalchemy.orm import relationship
from app.navy import navy_constants
from app.navy.navy_game_control import NavyGameControl
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, fields
from app import db
from app.models.user import User


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)

    id_user_1 = db.Column(db.Integer, db.ForeignKey(User.id))
    id_user_2 = db.Column(db.Integer, db.ForeignKey(User.id))
    user_1 = relationship("User", foreign_keys=[id_user_1])
    user_2 = relationship("User", foreign_keys=[id_user_2])

    def __init__(self, id_user_1=None, id_user_2=None):
        self.id_user_1 = id_user_1
        self.id_user_2 = id_user_2


  
class DynamicShip(db.Model):
    __tablename__ = "dynamic_ships"

    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey(Game.id))
    id_user = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)
    hp = db.Column(db.Integer)
    direction = db.Column(db.String(2))
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    ship_type = db.Column(db.Integer)

    game = db.relationship("Game", backref='ds', lazy=True)
    user = relationship("User")

    def __init__(self, id_game, id_user, hp, direction, pos_x, pos_y, ship_type):
        self.id_game = id_game
        self.id_user = id_user
        self.hp = hp
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ship_type = ship_type

class DynamicShipSchema(SQLAlchemySchema):

    class Meta:
        model = DynamicShip
        include_relationships = False
        load_instance = True

    id = auto_field()
    id_game = auto_field()
    id_user = auto_field()
    hp = auto_field()
    direction = auto_field()
    pos_x = auto_field()
    pos_y = auto_field()
    ship_type = auto_field()



class DynamicMissile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey(Game.id))
    id_ship = db.Column(db.Integer, db.ForeignKey(DynamicShip.id))
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    order = db.Column(db.Integer)
    direction = db.Column(db.String(2))
    missile_type = db.Column(db.Integer)

    game = relationship("Game")
    ship = relationship("DynamicShip")

    def __init__(self, id_game, id_ship, pos_x, pos_y, order, direction, missile_type):
        self.id_game = id_game
        self.id_ship = id_ship
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.order = order
        self.direction = direction
        self.missile_type = missile_type


class DynamicMissileSchema(SQLAlchemySchema):
    
        class Meta:
            model = DynamicMissile
            include_relationships = False
            load_instance = True
    
        id = auto_field()
        id_game = auto_field()
        id_ship = auto_field()
        pos_x = auto_field()
        pos_y = auto_field()
        order = auto_field()
        direction = auto_field()
        missile_type = auto_field()



class GameSchema(SQLAlchemySchema):
    class Meta:
        model = Game
        include_relationships = True
        load_instance = True


    cols = fields.Method('get_cols')
    rows = fields.Method('get_rows')
    data = fields.Method('get_data')

    def get_ships_static_data(self):
        dict = {
            "ships" : 
            NavyGameControl.read_data(navy_constants.PATH_TO_START)['ships_available'],
           "missiles" :
            NavyGameControl.read_data(navy_constants.PATH_TO_START)['missiles_available'] 
        }
        return dict

    def get_rows(self, obj):
        return navy_constants.ROWS

    def get_cols(self, obj):
        return navy_constants.COLS

    def get_dynamic_data(self):
        dict = {
              "ships" : DynamicShipSchema(many=True).dump(DynamicShip.query.filter_by(id_game=self.Meta.model.id).all()),
            "missiles" : DynamicMissileSchema(many=True).dump(DynamicMissile.query.filter_by(id_game=self.Meta.model.id).all())    
        }
        return dict

    def get_data(self, obj):
        dict = {
            "static_data" : self.get_ships_static_data(),
            "dynamic_data" : self.get_dynamic_data()
        }

        return dict
