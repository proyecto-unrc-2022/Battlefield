from ..command.command import Command


class UnderGameSession:
    def __init__(self, game, player1, player2):
        self.__game = game
        self.__players = [player1, player2]
        self.__turn = 0
        self.__order = 1  # 1 means forward, -1 means backward
        self.__commands = []
        self.__everyone_moved = False

        def add_command(self, c):
            if not isinstance(c, Command):
                raise TypeError("object is not a command")

            if c.player_id == self.__players[self.__turn]:
                self.__commands.append(c)

            return true

        def execute_commands(self):
            for c in self.__commands:
                c.execute()
            self.__comands.clear()

        def invert_order(self):
            self__order *= -1

        def everyone_moved(self):
            return self.__everyone_moved

        def get_game(self):
            return self.__game

        def get_players(self):
            return self.__players

        def get_order(self):
            return self.__order

        def get_turn(self):
            return self.__turn
