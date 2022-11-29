from app.models.airforce.utils import get_player_plane


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
        plane = get_player_plane(self.battlefield, self.player)[0]
        self.battlefield.move(plane, int(self.course))
