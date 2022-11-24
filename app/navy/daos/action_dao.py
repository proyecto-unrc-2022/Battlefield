from app import db
from app.navy.models.action import Action


class ActionDAO:
    def __init__(self, model):
        self.model = model

    def add_or_update(self, action):
        db.session.add(action)
        db.session.commit()

    def get_by_round(self, navy_game_id, round):
        return (
            db.session.query(self.model)
            .filter_by(navy_game_id=navy_game_id, round=round)
            .all()
        )

    def get_by_user_round(self, navy_game_id, round, user_id):
        return (
            db.session.query(self.model)
            .filter_by(navy_game_id=navy_game_id, round=round, user_id=user_id)
            .first()
        )


action_dao = ActionDAO(Action)
