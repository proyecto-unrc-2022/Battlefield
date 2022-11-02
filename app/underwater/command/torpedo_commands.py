from sqlalchemy.orm import relationship

from app import db

from ..daos.submerged_object_dao import submerged_object_dao
from .command import Command


class TorpedoCommand(Command):
    torpedo_id = db.Column(db.Integer, db.ForeignKey("torpedo.id"))

    torpedo = relationship("Torpedo")

    __mapper_args__ = {
        "polymorphic_identity": "torpedo_command",
        "polymorphic_on": Command.name,
    }

    def __init__(self, torpedo, **params):
        super(TorpedoCommand, self).__init__(torpedo.game, torpedo.player, **params)
        self.torpedo = torpedo


class AdvanceTorpedo(TorpedoCommand):
    __mapper_args__ = {
        "polymorphic_identity": "advance_torpedo",
    }

    def execute(self):
        if self.torpedo.in_game():
            self.game.advance_object(self.torpedo)
