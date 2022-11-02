from sqlalchemy.orm import relationship

from app import db

from .command import Command


class TorpedoCommand(Command):
    command_id = db.Column(db.Integer, db.ForeignKey("command.id"), primary_key=True)
    torpedo_id = db.Column(db.Integer, db.ForeignKey("torpedo.id"))

    torpedo = relationship("Torpedo")

    __mapper_args__ = {"polymorphic_identity": "torpedo_command"}

    def __init__(self, torpedo, **params):
        super(TorpedoCommand, self).__init__(torpedo.game, torpedo.player, **params)
        self.torpedo = torpedo


class AdvanceTorpedo(TorpedoCommand):
    torpedo_command_id = db.Column(
        db.Integer, db.ForeignKey("torpedo_command.command_id"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": "advance_torpedo"}

    def execute(self):
        if self.torpedo.in_game():
            self.game.advance_object(self.torpedo)
