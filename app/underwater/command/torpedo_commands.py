from ..daos.submerged_object_dao import submerged_object_dao
from .command import Command


class TorpedoCommand(Command):
    def __init__(self, torpedo, **params):
        super(TorpedoCommand, self).__init__(torpedo.game, torpedo.player, **params)
        self.torpedo_id = torpedo.id

    def get_torpedo(self):
        return submerged_object_dao.get_by_id(self.torpedo_id)


class AdvanceTorpedo(TorpedoCommand):
    def execute(self):
        torpedo = submerged_object_dao.get_by_id(self.torpedo_id)
        if torpedo.in_game():
            self.game.advance_object(torpedo)
