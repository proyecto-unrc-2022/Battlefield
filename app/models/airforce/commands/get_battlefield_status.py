class GetBattlefieldStatus:
    battlefield = None
    air_force_game = None
    player = None

    def __init__(self, battlefield, air_force_game, player):
        self.battlefield = battlefield
        self.air_force_game = air_force_game
        self.player = player

    def execute(self):
        if self.air_force_game.game_ended():
            return {"status": "end", "Winner": self.air_force_game.winner()}
        return self.battlefield.get_status_player(self.player)
