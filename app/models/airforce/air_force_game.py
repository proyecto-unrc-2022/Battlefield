from app.models.airforce.air_force_battlefield import Battlefield


class AirForceGame:
    player_a = None
    player_b = None
    battlefield = Battlefield()
    command = []
    turn = "a"
    player_a_ready = False
    player_b_ready = False

    def __init__(self):
        self.player_a = ""
        self.player_b = ""
        self.battlefield = Battlefield()
        self.command = []
        self.turn = "a"
        self.player_a_ready = False
        self.player_b_ready = False

    def add_command(self, command, player):
        self.command.append(command)
        self.ready(player)
        if self.player_a_ready and self.player_b_ready:
            self.executeList()

    def executeList(self):
        for c in self.command:
            c.execute()

    def execute(self, command):
        return command.execute()

    def ready(self, player):
        if player == self.player_a:
            self.player_a_ready = True
        else:
            self.player_b_ready = True

    def get_player_plane(self, player_id):
        return self.battlefield.get_player_plane(player_id)


class JoinGame:
    air_force_game = None
    player = None

    def __init__(self, air_force_game, player):
        self.air_force_game = air_force_game
        self.player = player

    def execute(self):

        if self.air_force_game.player_a == "":
            self.air_force_game.player_a = self.player
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

    def __init__(self, battlefield):
        self.battlefield = battlefield

    def execute(self):
        return self.battlefield.get_status()

    # def __str__(self):
    #     self.battlefield if self.battlefield is not None else "None"
    #     # self.battlefield.flying_obj if self.battlefield is not None else ""
