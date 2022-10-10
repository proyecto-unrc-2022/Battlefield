from app import db
from app.navy.models.ship import Ship


class ShipDAO:
    def __init__(self, model):
        self.model = model

    def add_or_update(self, ship):
        db.session.add(ship)
        db.session.commit()

    def delete(self, ship):
        db.session.delete(ship)
        db.session.commit()

    def get_by_id(self, ship_id):
        return Ship.query.filter_by(id=ship_id).first()

    def get_by_user(self, user_id):
        return Ship.query.filter_by(user_id == self.model.user_id)

    def get_by_game(self, navy_game_id):
        Ship.query.filter_by(navy_game_id == self.model.navy_game_id).all()

    def get_by(self, ship_id, user_id, navy_game_id):
        if ship_id:
            return Ship.query.filter_by(id=ship_id).first()
        return self.get_by_user(user_id) or self.get_by_game(navy_game_id)


ship_dao = ShipDAO(Ship)
