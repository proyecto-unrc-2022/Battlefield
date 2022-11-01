from app import db
from app.underwater.models.torpedo import Torpedo


class TorpedoLauncher:
    def create_torpedo(self, sub):
        torpedo = Torpedo(
            game=sub.game,
            player=sub.player,
            size=1,
            speed=sub.torpedo_speed,
            damage=sub.torpedo_damage,
        )
        return torpedo


t_launcher = TorpedoLauncher()
