from sqlalchemy.orm import backref, relationship

from app import db

from .submerged_object import SubmergedObject


class Torpedo(SubmergedObject):
    __tablename__ = "torpedo"
    id = db.Column(db.Integer, db.ForeignKey("submerged_object.id"), primary_key=True)
    damage = db.Column(db.Integer, nullable=False)

    player = relationship("User", backref=backref("torpedos"))

    # game = relationship("UnderGame", back_populates="torpedos")

    __mapper_args__ = {"polymorphic_identity": "torpedo"}
