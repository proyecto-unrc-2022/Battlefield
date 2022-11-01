import json

from sqlalchemy.orm import backref, relationship

from app import db

from .submerged_object import SubmergedObject


class Torpedo(SubmergedObject):
    __tablename__ = "torpedo"
    id = db.Column(db.Integer, db.ForeignKey("submerged_object.id"), primary_key=True)
    damage = db.Column(db.Integer, nullable=False)

    player = relationship("User", backref=backref("torpedos"))
    game = relationship("UnderGame", back_populates="torpedos")

    __mapper_args__ = {"polymorphic_identity": "torpedo"}

    def __init__(self, game, player, **params):
        self.game = game
        self.player = player
        self.size = 1
        self.speed = params["speed"]
        self.damage = params["damage"]
        if "x_position" in params.keys():
            self.x_position = params["x_position"]
        if "y_position" in params:
            self.y_position = params["y_position"]
        if "direction" in params.keys():
            self.direction = params["direction"]

    def to_dict(self):
        dict = {
            "player_id": self.player.id,
            "size": self.size,
            "speed": self.speed,
            "damage": self.damage,
        }
        if self.x_position:
            dict.update({"x_position": self.x_position})
        if self.y_position:
            dict.update({"y_position": self.y_position})
        if self.direction:
            dict.update({"direction": self.direction})
        if self.game:
            dict.update({"game_id:": self.game.id})
        return dict

    def __repr__(self):
        return json.dumps(self.to_dict())
