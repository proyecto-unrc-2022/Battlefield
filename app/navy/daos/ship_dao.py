from app import db
from app.navy.models.ship import Ship


class ShipDAO:
    def __init__(self, model):
        self.model = model

    def add(self, ship):
        db.session.add(ship)
        db.session.commit()
        return ship

    def update(self, ship, commit=False):
        db.session.add(ship)
        if commit:
            db.session.commit()

    def update_all(self, ships, commit=False):
        db.session.add_all(ships)
        if commit:
            db.session.commit()

    def get_by_id(self, ship_id):
        return db.session.query(self.model).filter_by(id=ship_id).first()

    def get_by(self, user_id=None, navy_game_id=None, ship_id=None):
        return (
            db.session.query(self.model)
            .filter(
                user_id == self.model.user_id if user_id else True,
                navy_game_id == self.model.navy_game_id if navy_game_id else True,
                ship_id == self.model.id if ship_id else True,
            )
            .all()
        )


ship_dao = ShipDAO(Ship)
