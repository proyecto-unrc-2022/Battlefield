from .command import Command


class SubmarineCommand(Command):
    def __init__(self, game, submarine, **params):
        super(SubmarineCommand, self).__init__(game, submarine.player, **params)
        self.submarine = submarine

    def get_submarine(self):
        return self.submarine


class RotateAndAdvance(SubmarineCommand):
    def execute(self):
        self.game.rotate_object(self.submarine, self.params["direction"])
        if self.submarine.in_game():
            self.game.advance_object(self.submarine, self.params["steps"])


class RotateAndAttack(SubmarineCommand):
    def __init__(self, game, submarine, **params):
        super(RotateAndAttack, self).__init__(game, submarine, **params)

    def execute(self):
        self.game.rotate_object(self.submarine, self.params["direction"])
        if self.submarine.in_game():
            self.game.attack(self.submarine)
