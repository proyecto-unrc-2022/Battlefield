from app import db
from sqlalchemy.orm import relationship

from .submerged_object import SubmergedObject

class Torpedo(SubmergedObject):
    id = db.Column(db.Integer, db.ForeignKey("submerged_object.id"), primary_key=True)
    damage = db.Column(db.Integer, nullable=False)

    #game = relationship("UnderGame", back_populates="torpedos")

    __mapper_args__ = {
        "polymorphic_identity": "torpedo"
    }