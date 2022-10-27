from app import db
from app.underwater.models.torpedo import Torpedo


class TorpedoLauncher:
    def create_torpedo(self, sub):
        x, y = sub.get_next_position()
        torpedo = Torpedo(
            game_id=sub.game_id,
            player_id=sub.player_id,
            x_position=x,
            y_position=y,
            direction=sub.direction,
            size=1,
            speed=sub.torpedo_speed,
            damage=sub.torpedo_damage,
        )
        db.session.add(torpedo)  # No se si gusta mucho que toque bd
        db.session.commit()
        return torpedo


t_launcher = TorpedoLauncher()
