class GetPlayers:
    air_force_game = None

    def __init__(self, air_force_game):
        self.air_force_game = air_force_game

    def execute(self):
        return {
            "player_a": self.air_force_game.player_a,
            "player_b": self.air_force_game.player_b,
        }
