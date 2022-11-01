import json

from app.daos.user_dao import get_user_by_id
from app.underwater.daos.under_game_dao import game_dao

from ..command import Command, SubmarineCommand


class UnderGameSession:
    def __init__(self, host, *visitors):
        self.__players_ids = [host.id]
        for player in visitors:
            self.__players_ids.append(player.id)
        self.__turn = 0
        self.__order = 1  # 1 means forward, -1 means backward
        self.__commands = []
        self.__remaining_to_move = self.__players_ids.copy()
        self.game = None
        self.id = None

    @staticmethod
    def start_session_for(game):
        new_session = UnderGameSession(game.host)
        if game.visitor:
            new_session.add_player(game.visitor)

        new_session.game = game
        new_session.id = game.id
        return new_session

    def set_game(self, game):
        self.game = game
        self.id = game.id

    def add_command(self, c):
        if not isinstance(c, Command):
            raise TypeError("object is not a command")

        player = c.get_player()
        if player.id is self.__players_ids[self.__turn]:
            self.__commands.append(c)
            if isinstance(c, SubmarineCommand):
                self.__remaining_to_move.remove(player.id)
            return True

        return False

    def next_turn(self):
        self.__turn += self.__order

    def add_player(self, player):
        if player.id in self.__players_ids:
            return False

        self.__players_ids.append(player.id)
        self.__remaining_to_move.append(player.id)
        return True

    def execute_commands(self):
        for c in self.__commands:
            c.execute()
        self.__commands.clear()
        self.__remaining_to_move = self.__players_ids.copy()

    def invert_order(self):
        self.__order *= -1

    def everyone_moved(self):
        return self.__remaining_to_move == []

    def get_game(self):
        return self.game

    def get_players(self):
        players = []
        for player_id in self.__players_ids:
            players.append(get_user_by_id(player_id))
        return players

    def get_order(self):
        return self.__order

    def remaining_to_move(self):
        return self.__remaining_to_move

    def get_turn(self):
        return self.__turn

    def get_commands(self):
        return self.__commands

    def current_turn_player(self):
        return get_user_by_id(self.__players_ids[self.__turn])

    def set_turn(self, player):
        for i in range(len(self.__players_ids)):
            if self.__players_ids[i] == player.id:
                self.__turn = i
                return

    def clear(self):
        self.__turn = 0
        self.__order = 1
        self.__commands = []
        self.__remaining_to_move = self.__players_ids.copy()

    def to_dict(self):
        # commands_to_dict = []  esto iria?
        # i = 1
        # for c in self.__commands:
        #     commands_to_dict.update({"{}".format(i): c.__repr__()})
        #     i += 1
        dict = {
            "turn": self.__turn,
            "order": self.__order  # ,
            # "commands": commands_to_dict,
            # "game": self.game.to_dict
            # "remaining_to_move" lo ponemos?
        }
        dict.update(self.game.to_dict())  # append game dict to this dict
        return dict

    def __repr__(self):
        return json.dumps(self.to_dict())
