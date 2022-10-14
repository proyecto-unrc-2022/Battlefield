from .command import Command


class SubmarineCommand(Command):
    def __init__(self, game, submarine, params):
        self.__game = game
        self.__submarine = submarine
        self.__params = params


class RotateAndAdvance(SubmarineCommand):
    def execute(self):
        self.__game.rotate_object(__submarine, __params["direction"])
        if __submarine.in_game():
            self.__game.advance_object(__submarine, __params["steps"])


class RotateAndAttack(SubmarineCommand):
    def execute(self):
        self.__game.rotate_object(__submarine, __params["direction"])
        if __submarine.in_game():
            self.__game.attack(__submarine)
