from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, fields
from sqlalchemy.orm import relationship

from app import db
from app.models.navy.dynamic_game import Game
from app.models.user import User
from app.navy import navy_constants


class DynamicShip(db.Model):

    __tablename__ = "dynamic_ships"

    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey("game.id"))
    id_user = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)
    hp = db.Column(db.Integer)
    direction = db.Column(db.String(2))
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    ship_type = db.Column(db.Integer)

    game = relationship("Game", backref="ships", lazy=True)

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
