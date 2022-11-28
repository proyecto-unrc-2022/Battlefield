import json

from sqlalchemy.orm import backref, relationship

from app import db
from app.underwater.torpedo_launcher import t_launcher

from .submerged_object import SubmergedObject


class Submarine(SubmergedObject):
    __tablename__ = "submarine"
    id = db.Column(db.Integer, db.ForeignKey("submerged_object.id"), primary_key=True)
    name = db.Column(db.String(50))
    visibility = db.Column(db.Integer, nullable=False)
    radar_scope = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Float, nullable=False)
    torpedo_speed = db.Column(db.Integer, nullable=False)
    torpedo_damage = db.Column(db.Float, nullable=False)

    under_board_mask = relationship(
        "BoardMask", back_populates="submarine", uselist=False, cascade="all, delete"
    )

    player = relationship("User", backref=backref("submarine", uselist=False))
    game = relationship("UnderGame", back_populates="submarines")

    __mapper_args__ = {"polymorphic_identity": "submarine"}

    def __init__(
        self, game, player, stats, x_position=None, y_position=None, direction=None
    ):
        self.game = game
        self.player = player
        self.name = stats["name"]
        self.size = stats["size"]
        self.speed = stats["speed"]
        self.visibility = stats["visibility"]
        self.radar_scope = stats["radar_scope"]
        self.health = stats["health"]
        self.torpedo_speed = stats["torpedo_speed"]
        self.torpedo_damage = stats["torpedo_damage"]

        if x_position is not None:
            self.x_position = x_position
        if y_position is not None:
            self.y_position = y_position
        if direction is not None:
            self.direction = direction

    def create_torpedo(self):
        return t_launcher.create_torpedo(self)

    def to_dict(self):
        dict = {
            "player_id": self.player_id,
            "name": self.name,
            "size": self.size,
            "speed": self.speed,
            "visibility": self.visibility,
            "radar_scope": self.radar_scope,
            "health": self.health,
            "torpedo_speed": self.torpedo_speed,
            "torpedo_damage": self.torpedo_damage,
        }
        if self.x_position is not None:
            dict.update({"x_position": self.x_position})
        if self.y_position is not None:
            dict.update({"y_position": self.y_position})
        if self.direction is not None:
            dict.update({"direction": self.direction})
        if self.game:
            dict.update({"game_id:": self.game.id})
        return dict

    def public_dict(self):
        dict = {
            "player_id": self.player_id,
            "name": self.name,
            "size": self.size,
            "speed": self.speed,
            "visibility": self.visibility,
            "radar_scope": self.radar_scope,
            "health": self.health,
            "torpedo_speed": self.torpedo_speed,
            "torpedo_damage": self.torpedo_damage,
        }
        return dict

    def __get_nearest_cells(self, delta):
        positions = []
        min_x = self.x_position - delta
        min_y = self.y_position - delta
        max_x = self.x_position + delta
        max_y = self.y_position + delta

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.game.board.valid((x, y)):
                    positions.append((x, y))

        return positions

    def get_vision_scope(self):
        return self.__get_nearest_cells(self.visibility)

    def get_radar_scope(self):
        return self.__get_nearest_cells(self.radar_scope)

    def __repr__(self):
        return json.dumps(self.to_dict())

    def update_visibility(self):
        self.under_board_mask.update()
