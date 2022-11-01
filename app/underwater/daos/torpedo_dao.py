from app import db
from app.underwater.models import Torpedo


class TorpedoDAO(SubmergedObjectDAO):
    def create(self, game, player, **params):
        torpedo = Torpedo(game, player, **params)
        db.session.add(torpedo)
        db.session.commit()
