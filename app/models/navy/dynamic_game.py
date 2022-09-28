from __future__ import annotations

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, fields
from sqlalchemy.orm import relationship

from app import db
from app.models.user import User
from app.navy import navy_constants


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

    cols = fields.Method("get_cols")
    rows = fields.Method("get_rows")
    data = fields.Method("get_data")

    def get_ships_static_data(self):
        from app.daos.navy.game_dao import read_data

        dict = {
            "ships": read_data(navy_constants.PATH_TO_START)["ships_available"],
            "missiles": read_data(navy_constants.PATH_TO_START)["missiles_available"],
        }
        return dict

    def get_rows(self, obj):
        return navy_constants.ROWS

    def get_cols(self, obj):
        return navy_constants.COLS

    def get_dynamic_data(self):
        from app.daos.navy.dynamic_missile_dao import get_missiles
        from app.daos.navy.dynamic_ship_dao import get_ships

        from .dynamic_missile import DynamicMissileSchema
        from .dynamic_ship import DynamicShipSchema

        dict = {
            "ships": DynamicShipSchema(many=True).dump(get_ships(self.Meta.model.id)),
            "missiles": DynamicMissileSchema(many=True).dump(
                get_missiles(self.Meta.model.id)
            ),
        }
        return dict

    def get_data(self, obj):
        dict = {
            "static_data": self.get_ships_static_data(),
            "dynamic_data": self.get_dynamic_data(),
        }

        return dict
