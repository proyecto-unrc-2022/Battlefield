from sqlalchemy.orm import relationship

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

    __mapper_args__ = {"polymorphic_identity": "submarine"}

    def create_torpedo(self):
        return t_launcher.create_torpedo(self)

    def set_health(self, health):
        self.health = health
