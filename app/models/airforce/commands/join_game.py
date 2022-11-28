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
            if self.air_force_game.player_a == self.player:
                raise Exception("Players must be differents")
            self.air_force_game.player_b = self.player
        else:
            raise Exception("The game is full!")
