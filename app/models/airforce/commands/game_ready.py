class GameReady:
    game: None

    def __init__(self, game):
        self.game = game

    def execute(self):
        ready = self.game.player_a != "" and self.game.player_b != ""
        return {"status": ready}
