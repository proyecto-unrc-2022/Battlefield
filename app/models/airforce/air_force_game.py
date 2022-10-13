from app.models.airforce.air_force_battlefield import Battlefield


class AirForceGame:
    player_a = None
    player_b = None
    battlefield = Battlefield()

    def join_game(self, new_player):
        if self.player_a == None:
            self.player_a = new_player
        elif self.player_b == None:
            self.player_b = new_player
        else:
            raise Exception("The game are full!")
        return {"player_a": self.player_a, "player_b": self.player_b}

    def get_player_plane(self, player_id):
        return self.battlefield.get_player_plane(player_id)
