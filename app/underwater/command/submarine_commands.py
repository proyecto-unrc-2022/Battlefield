from app.underwater.daos.submarine_dao import submarine_dao

from .command import Command


class SubmarineCommand(Command):
    def __init__(self, game, submarine, **params):
        super(SubmarineCommand, self).__init__(game, submarine.player, **params)
        self.submarine = submarine

    def get_submarine(self):
        return self.submarine


class RotateAndAdvance(SubmarineCommand):
    def execute(self):
        submarine = self.submarine
        if submarine.in_game():
            self.game.rotate_object(submarine, self.params["direction"])
            if submarine.in_game():
                self.game.advance_object(submarine, self.params["steps"])


class RotateAndAttack(SubmarineCommand):
    def execute(self):
        submarine = self.submarine
        if submarine.in_game():
            self.game.rotate_object(submarine, self.params["direction"])
            if submarine.in_game():
                self.game.attack(submarine)
