class Command:
    def __init__(self, game, player, **params):
        self.game = game
        self.player = player
        self.params = params

    def execute(self):
        raise NotImplementedError()

    def get_game(self):
        return self.game

    def get_player(self):
        return self.player

    def get_params(self):
        return self.params
