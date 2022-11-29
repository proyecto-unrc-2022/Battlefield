from app.models.airforce.plane import Projectile
from app.models.airforce.utils import (
    discount_projectile,
    get_player_plane,
    projectile_avaible,
)


class LaunchProjectile:
    player = None
    air_force_game = None
    battlefield = None

    def __init__(self, player, air_force_game):
        if not projectile_avaible(player, air_force_game.battlefield):
            raise Exception("No enough projectile")
        self.player = player
        self.air_force_game = air_force_game
        self.battlefield = air_force_game.battlefield

    def execute(self):
        plane = get_player_plane(self.battlefield, int(self.player))[0]
        course = plane.course
        x = plane.x
        y = plane.y

        plane_model = plane.flying_obj

        projectile = Projectile.query.filter_by(plane_id=plane_model.id).first()

        if course == 1:
            y = y - 1
        elif course == 2:
            x = x + 1
        elif course == 3:
            y = y + 1
        elif course == 4:
            x = x - 1
        discount_projectile(self.player, self.battlefield)
        return self.battlefield.add_new_flying_object(
            self.player, projectile, x, y, course
        )
