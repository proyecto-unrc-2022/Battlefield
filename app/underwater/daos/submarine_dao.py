from app import db

from ..models.submarine import Submarine
from .submerged_object_dao import SubmergedObjectDAO


class SubmarineDAO(SubmergedObjectDAO):
    def __init__(self, model):
        self.model = model

    def create_submarine(
        self,
        game_id,
        player_id,
        stats,
        x_position=None,
        y_position=None,
        direction=None,
    ):
        sub = self.model(game_id, player_id, stats)
        if x_position and y_position and direction:
            sub.set_direction(x_position, y_position, direction)
        db.session.add(sub)
        db.session.commit()
        return sub

    def get_by_id(self, sub_id):
        sub = db.session.get(self.model, sub_id)
        if not sub:
            raise ValueError("no submarine found with id %s" % sub_id)
        return sub

    def save(self, sub):
        db.session.add(sub)
        db.session.commit()


submarine_dao = SubmarineDAO(Submarine)
