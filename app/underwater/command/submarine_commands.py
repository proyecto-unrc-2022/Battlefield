from app.underwater.daos.submarine_dao import submarine_dao

from .command import Command


class SubmarineCommand(Command):
    def __init__(self, game, submarine, **params):
        super(SubmarineCommand, self).__init__(game, submarine.player, **params)
        self.submarine_id = submarine.id

    def get_submarine(self):
        return submarine_dao.get_by_id(self.submarine_id)


class RotateAndAdvance(SubmarineCommand):
    def execute(self):
        submarine = submarine_dao.get_by_id(self.submarine_id)
        self.game.rotate_object(submarine, self.params["direction"])
        if submarine.in_game():
            self.game.advance_object(submarine, self.params["steps"])


class RotateAndAttack(SubmarineCommand):
    def execute(self):
        submarine = submarine_dao.get_by_id(self.submarine_id)
        self.game.rotate_object(submarine, self.params["direction"])
        if submarine.in_game():
            self.game.attack(submarine)
