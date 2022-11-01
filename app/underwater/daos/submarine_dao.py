from app import db
from app.underwater.models import Submarine

from .submerged_object_dao import SubmergedObjectDAO


class SubmarineDAO(SubmergedObjectDAO):
    def create_submarine(
        self,
        game_id,
        player_id,
        stats,
        x_position=None,
        y_position=None,
        direction=None,
    ):
        sub = self.Submarine(game_id, player_id, stats)
        sub.x_position = x_position
        sub.y_position = y_position
        sub.direction = direction
        self.save(sub)
        return sub

    def get_by_id(self, sub_id):
        return db.session.get(Submarine, sub_id)

    def save(self, sub):
        db.session.add(sub)
        db.session.commit()


submarine_dao = SubmarineDAO()
