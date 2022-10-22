from app import db
from app.underwater.models.torpedo import Torpedo


class TorpedoLauncher:
    def create_torpedo(self, sub):
        x, y = sub.get_next_position()
        torpedo = Torpedo(
            game=sub.game,
            player=sub.player,
            # x_position=x,
            # y_position=y,
            # direction=sub.direction,
            size=1,
            speed=sub.torpedo_speed,
            damage=sub.torpedo_damage,
        )
        return torpedo


t_launcher = TorpedoLauncher()
