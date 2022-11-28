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
