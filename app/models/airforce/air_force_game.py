from hashlib import new

from app.models.airforce.air_force_battlefield import Battlefield


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
        return self.battlefield.get_player_plane(player_id)

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
            self.get_player_plane(self.player_a) == []
            or self.get_player_plane(self.player_b) == []
        ):
            return True
        return False

    def winner(self):
        if self.get_player_plane(self.player_a) == []:
            return self.player_b
        elif self.get_player_plane(self.player_b) == []:
            return self.player_a
        return None


class JoinGame:
    air_force_game = None
    player = None

    def __init__(self, air_force_game, player):
        self.air_force_game = air_force_game
        self.player = player

    def execute(self):

        if self.air_force_game.player_a == "":
            self.air_force_game.player_a = self.player
            self.air_force_game.turn = self.player
        elif self.air_force_game.player_b == "":
            self.air_force_game.player_b = self.player
        else:
            raise Exception("The game is full!")


class GetPlayers:
    air_force_game = None

    def __init__(self, air_force_game):
        self.air_force_game = air_force_game

    def execute(self):
        return {
            "player_a": self.air_force_game.player_a,
            "player_b": self.air_force_game.player_b,
        }


class ChoosePlane:
    course = None
    x = None
    y = None
    player = None
    battlefield = None
    plane = None
    air_force_game = None

    def __init__(self, course, x, y, player, plane, air_force_game):
        self.course = course
        self.x = x
        self.y = y
        self.player = player
        self.battlefield = air_force_game.battlefield
        self.plane = plane
        self.air_force_game = air_force_game

    def execute(self):
        return self.battlefield.add_new_plane(
            int(self.player),
            self.plane,
            int(self.x),
            int(self.y),
            int(self.course),
            self.air_force_game,
        )


class MovePlane:
    course = None
    player = None
    battlefield = None
    air_force_game = None

    def __init__(self, course, player, air_force_game):
        self.course = course
        self.player = player
        self.battlefield = air_force_game.battlefield
        self.air_force_game = air_force_game

    def execute(self):
        self.battlefield.fligth(int(self.player), int(self.course))


class LaunchProjectile:
    player = None
    air_force_game = None
    battlefield = None

    def __init__(self, player, air_force_game):
        self.player = player
        self.air_force_game = air_force_game
        self.battlefield = air_force_game.battlefield

    def execute(self):
        return self.battlefield.add_new_projectile(self.player)


class Shoot:
    player = None
    battlefield = None

    def __init__(self, course, player, battlefield):
        self.course = course
        self.player = player
        self.battlefield = battlefield

    def execute(self):
        raise NotImplementedError()


class GetBattlefieldStatus:
    battlefield = None
    air_force_game = None

    def __init__(self, battlefield, air_force_game):
        self.battlefield = battlefield
        self.air_force_game = air_force_game

    def execute(self):
        if self.air_force_game.game_ended():
            return {"status": "end", "Winner": self.air_force_game.winner()}
        return self.battlefield.get_status()

    # def __str__(self):
    #     self.battlefield if self.battlefield is not None else "None"
    #     # self.battlefield.flying_obj if self.battlefield is not None else ""


class CheckCourse:
    course: None
    game: None
    player: None

    def __init__(self, course, player, game):
        self.course = course
        self.game = game
        self.player = player

    def execute(self):
        self.game.battlefield.check_course(self.course, self.player)


class GameReady:
    game: None

    def __init__(self, game):
        self.game = game

    def execute(self):
        ready = self.game.player_a != [] and self.game.player_b != []
        return {"status": ready}


class PlayersHavePlane:
    game: None

    def __init__(self, game):
        self.game = game

    def execute(self):
        ready = (
            self.game.battlefield.get_player_plane(self.game.player_a) != []
            and self.game.battlefield.get_player_plane(self.game.player_b) != []
        )

        return {"status": ready}
