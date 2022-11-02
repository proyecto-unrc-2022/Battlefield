from sqlalchemy.orm import relationship

from app import db
from app.underwater.daos.submarine_dao import submarine_dao

from .command import Command


class SubmarineCommand(Command):
    submarine_id = db.Column(db.Integer, db.ForeignKey("submarine.id"))
    direction = db.Column(db.Integer)

    submarine = relationship("Submarine")

    __mapper_args__ = {
        "polymorphic_identity": "submarine_command",
        "polymorphic_on": Command.name,
    }

    def __init__(self, game, submarine, **params):
        super(SubmarineCommand, self).__init__(game, submarine.player, **params)
        self.submarine = submarine

    def get_submarine(self):
        return self.submarine


class RotateAndAdvance(SubmarineCommand):
    steps = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "rotate_and_advance",
    }

    def __init__(self, game, submarine, **params):
        super().__init__(game, submarine, **params)
        self.direction = params["direction"]
        self.steps = params["steps"]

    def execute(self):
        submarine = self.submarine
        if submarine.in_game():
            self.game.rotate_object(submarine, self.params["direction"])
            if submarine.in_game():
                self.game.advance_object(submarine, self.params["steps"])


class RotateAndAttack(SubmarineCommand):
    __mapper_args__ = {
        "polymorphic_identity": "rotate_and_attack",
    }

    def __init__(self, game, submarine, **params):
        super().__init__(game, submarine, **params)
        self.direction = params["direction"]

    def execute(self):
        submarine = self.submarine
        if submarine.in_game():
            self.game.rotate_object(submarine, self.params["direction"])
            if submarine.in_game():
                self.game.attack(submarine)
