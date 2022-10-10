from app import db
from app.navy.models.action import Action


class ActionDAO:

    def __init__(self, model):
        self.model = model

    def add_or_update_action(self, action):
        db.session.add(action)
        db.session.commit()

    def delete_action(self, action):
        db.session.delete(action)
        db.session.commit()

    def get_by_user(user_id, navy_game_id):
        return db.session.execute(db.select(Action).filter_by(user_id=user_id,navy_game_id=navy_game_id)).one()
            

action_dao = ActionDAO(Action)