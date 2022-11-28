from sqlalchemy import or_

from app import db
from app.navy.models.navy_game import NavyGame


class NavyGameDao:
    def __init__(self, model):
        self.model = model

    def add(self, navy_game):
        db.session.add(navy_game)
        db.session.commit()

    def update(self, navy_game, commit=False):
        db.session.add(navy_game)
        if commit:
            db.session.commit()

    def get_all(self):
        return db.session.query(self.model).all()

    def get_by_user(self, user_id):
        return (
            db.session.query(self.model)
            .filter(or_(self.model.user1_id == user_id, self.model.user2_id == user_id))
            .all()
        )

    def get_by_id(self, navy_game_id):
        return db.session.query(self.model).filter_by(id=navy_game_id).first()

    def delete(self, navy_game):
        db.session.delete(navy_game)
        db.session.commit()


navy_game_dao = NavyGameDao(NavyGame)
