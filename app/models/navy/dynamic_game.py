from sqlalchemy.orm import relationship
from app.navy import navy_constants

from app.navy.navy_game_control import NavyGameControl
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, fields
from app import db
from app.models.user import User


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_user_1 = db.Column(db.Integer, db.ForeignKey(User.id))
    id_user_2 = db.Column(db.Integer, db.ForeignKey(User.id))
    user_1 = relationship("User", foreign_keys=[id_user_1])
    user_2 = relationship("User", foreign_keys=[id_user_2])

    def __init__(self, id_user_1=None, id_user_2=None):
        self.id_user_1 = id_user_1
        self.id_user_2 = id_user_2


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
        from .dynamic_ship  import DynamicShip, DynamicShipSchema
        from .dynamic_missile import DynamicMissile, DynamicMissileSchema
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
