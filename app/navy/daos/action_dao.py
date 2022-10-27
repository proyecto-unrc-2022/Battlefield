from app import db
from app.navy.models.action import Action


class ActionDAO:
    def __init__(self, model):
        self.model = model

    def add_or_update(self, action):
        db.session.add(action)
        db.session.commit()

    def delete(self, action):
        db.session.delete(action)
        db.session.commit()

    def get_by_user(self, user_id, navy_game_id):
        return (
            db.session.query(self.model)
            .filter_by(user_id=user_id, navy_game_id=navy_game_id)
            .one()
        )

    def get_by_round(self, navy_game_id, round):
        return (
            db.session.query(self.model)
            .filter_by(navy_game_id=navy_game_id, round=round)
            .all()
        )


action_dao = ActionDAO(Action)
