from sqlalchemy.orm import relationship

from app import db

from .command import Command


class SubmarineCommand(Command):
    command_id = db.Column(db.Integer, db.ForeignKey("command.id"), primary_key=True)
    submarine_id = db.Column(db.Integer, db.ForeignKey("submarine.id"))
    direction = db.Column(db.Integer)

    submarine = relationship("Submarine")

    __mapper_args__ = {
        "polymorphic_identity": "submarine_command",
    }

    def __init__(self, game, submarine, **params):
        super().__init__(game, submarine.player, **params)
        self.submarine = submarine

    def get_submarine(self):
        return self.submarine


class RotateAndAdvance(SubmarineCommand):
    submarine_command_id = db.Column(
        db.Integer, db.ForeignKey("submarine_command.command_id"), primary_key=True
    )
    steps = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "rotate_and_advance"}

    def __init__(self, game, submarine, **params):
        super().__init__(game, submarine, **params)
        self.direction = params["direction"]
        self.steps = params["steps"]

    def execute(self):
        submarine = self.submarine
        if submarine.in_game():
            self.game.rotate_object(submarine, self.direction)
            if submarine.in_game():
                self.game.advance_object(submarine, self.steps)


class RotateAndAttack(SubmarineCommand):
    submarine_command_id = db.Column(
        db.Integer, db.ForeignKey("submarine_command.command_id"), primary_key=True
    )
    __mapper_args__ = {"polymorphic_identity": "rotate_and_attack"}

    def __init__(self, game, submarine, **params):
        super().__init__(game, submarine, **params)
        self.direction = params["direction"]

    def execute(self):
        if self.submarine.in_game():
            self.game.rotate_object(self.submarine, self.direction)
            if self.submarine.in_game():
                self.game.attack(self.submarine)


class SendRadarPulse(SubmarineCommand):
    submarine_command_id = db.Column(
        db.Integer, db.ForeignKey("submarine_command.command_id"), primary_key=True
    )
    __mapper_args__ = {"polymorphic_identity": "rotate_and_attack"}

    def __init__(self, game, submarine, **params):
        super().__init__(game, submarine, **params)

    def execute(self):
        if self.submarine.in_game():
            self.game.send_radar_pulse(self.submarine)
        print(f"Submarine {self.submarine.id} sends radar pulse")
