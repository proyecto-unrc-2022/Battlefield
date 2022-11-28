from app.models.airforce.utils import get_player_plane


class PlayersHavePlane:
    game: None

    def __init__(self, game):
        self.game = game

    def execute(self):
        ready = (
            get_player_plane(self.game.battlefield, self.game.player_a) != []
            and get_player_plane(self.game.battlefield, self.game.player_b) != []
        )

        return {"status": ready}
