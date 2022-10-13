from sqlalchemy.orm import relationship

from app import db
from app.navy.models.navy_game import NavyGame


class Missile(db.Model):
    __tablename__ = "missiles"

    id = db.Column(db.Integer, primary_key=True)
    speed = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    course = db.Column(db.Integer)
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    ship_id = db.Column(db.Integer, db.ForeignKey("ships.id"))
    navy_game_id = db.Column(
        db.Integer, db.ForeignKey("navy_games.id", ondelete="CASCADE")
    )
    order = db.Column(db.Integer)

    def __init__(
        self, speed, damage, course, pos_x, pos_y, ship_id, navy_game_id, order
    ):
        self.speed = speed
        self.damage = damage
        self.course = course
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ship_id = ship_id
        self.navy_game_id = navy_game_id
        self.order = order

    from app.navy.models.navy_game import NavyGame

    navy_game = relationship("NavyGame", back_populates="missiles")
    ship = relationship("Ship", back_populates="missiles")
