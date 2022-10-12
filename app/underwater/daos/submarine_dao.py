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
        sub = self.model(
            game_id=game_id,
            player_id=player_id,
            name=stats["name"],
            size=stats["size"],
            speed=stats["speed"],
            visibility=stats["visibility"],
            radar_scope=stats["radar_scope"],
            health=stats["health"],
            torpedo_speed=stats["torpedo_speed"],
            torpedo_damage=stats["torpedo_damage"],
        )
        if x_position:
            sub.x_position = x_position
        if y_position:
            sub.y_position = y_position
        if direction:
            sub.direction = direction
        db.session.add(sub)
        db.session.commit()
        return sub

    def get_by_id(self, sub_id):
        sub = db.session.get(self.model, sub_id)
        if not sub:
            raise ValueError("no submarine found with id %s" % sub_id)
        return sub


submarine_dao = SubmarineDAO(Submarine)
