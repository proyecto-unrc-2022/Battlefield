from app import db
from app.navy.models.missile import Missile


class MissileDAO:
    def __init__(self, model):
        self.model = model

    def add(self, missile):
        db.session.add(missile)
        db.session.commit()
        return missile

    def update_all(self, missiles):
        db.session.add_all(missiles)

    def get_by_navy_game_id(self, navy_game_id):
        return db.session.query(self.model).filter_by(navy_game_id=navy_game_id).all()


missile_dao = MissileDAO(Missile)
