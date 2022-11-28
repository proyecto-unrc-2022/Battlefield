from app.models.airforce.air_force_battlefield import Battlefield
from app.models.airforce.airforce_filters import get_player_plane


class AirForceGame:
    player_a = None
    player_b = None
    battlefield = Battlefield()
    new_commands = {}
    turn = "a"
    player_a_ready = False
    player_b_ready = False

    def __init__(self):
        self.player_a = ""
        self.player_b = ""
        self.battlefield = Battlefield()
        self.new_commands = {"first": [], "second": []}
        self.turn = None
        self.player_a_ready = False
        self.player_b_ready = False
        self.old_commands = []

    def add_command(self, command, player):

        if self.player_cant_add_command(player):
            raise Exception("only one command per turn")

        if player == self.turn:
            self.new_commands.get("first").append(command)
        else:
            self.new_commands.get("second").append(command)

        self.ready(player)
        if self.player_a_ready and self.player_b_ready:
            self.executeList()
            self.update_turn()

    def executeList(self):
        if self.turn != self.player_a and not self.game_ended():
            self.battlefield.move_projectile(self.player_a)
            if not self.game_ended():
                self.battlefield.move_projectile(self.player_b)
        else:
            if not self.game_ended():
                self.battlefield.move_projectile(self.player_b)
            if not self.game_ended():
                self.battlefield.move_projectile(self.player_a)
        if not self.game_ended():
            for c in self.new_commands.get("first"):
                c.execute()
            for c in self.new_commands.get("second"):
                c.execute()
        self.new_commands.get("first").clear()
        self.new_commands.get("second").clear()
        self.player_a_ready = False
        self.player_b_ready = False

    def execute(self, command):
        return command.execute()

    def ready(self, player):
        if player == self.player_a:
            self.player_a_ready = True
            self.turn = player
        else:
            self.player_b_ready = True

    def get_player_plane(self, player_id):
        return get_player_plane(self.battlefield, player_id)

    def player_cant_add_command(self, player):
        if player == self.player_a and self.player_a_ready:
            return True
        elif player == self.player_b and self.player_b_ready:
            return True
        return False

    def update_turn(self):
        self.turn = self.player_b if (self.turn == self.player_a) else self.player_a

    def game_ended(self):
        if (
            get_player_plane(self.battlefield, self.player_a) == []
            or get_player_plane(self.battlefield, self.player_b) == []
        ):
            return True
        return False

    def winner(self):
        if self.get_player_plane(self.player_a) == []:
            return self.player_b
        elif self.get_player_plane(self.player_b) == []:
            return self.player_a
        return None
