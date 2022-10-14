from .command import Command


class TorpedoCommand(Command):
    def __init__(self, game, torpedo, params):
        self.__game = game
        self.__torpedo = torpedo
        self.__params = params


class AdvanceTorpedo(TorpedoCommand):
    def execute(self):
        __game.advance_object(self.__torpedo)
