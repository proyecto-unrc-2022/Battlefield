from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, fields
from app.models.navy.dynamic_game import Game
from sqlalchemy.orm import relationship

from app import db
from app.models.user import User


class DynamicMissile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey("game.id"))
    id_ship = db.Column(db.Integer, db.ForeignKey("dynamic_ships.id"))
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    order = db.Column(db.Integer)
    direction = db.Column(db.String(2))
    missile_type = db.Column(db.Integer)

    game = relationship("Game", backref="missiles", lazy=True)

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
