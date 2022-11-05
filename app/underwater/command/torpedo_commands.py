from ..daos.submerged_object_dao import submerged_object_dao
from .command import Command


class TorpedoCommand(Command):
    def __init__(self, torpedo, **params):
        super(TorpedoCommand, self).__init__(torpedo.game, torpedo.player, **params)
        self.torpedo = torpedo

    def get_torpedo(self):
        return self.torpedo


class AdvanceTorpedo(TorpedoCommand):
    def execute(self):
        if self.torpedo.in_game():
            self.game.advance_object(self.torpedo)
