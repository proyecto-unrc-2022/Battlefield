from app.models.airforce.utils import player_have_plane, position_inside_player_field


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
        if not position_inside_player_field(
            self.battlefield.max_x,
            self.x,
            self.course,
            self.player,
            self.air_force_game,
        ):
            raise Exception("Plane position cant be inside enemy field")
        if player_have_plane(self.battlefield, self.player):
            raise Exception("This player already have a plane")

        return self.battlefield.add_new_flying_object(
            int(self.player), self.plane, int(self.x), int(self.y), int(self.course)
        )
