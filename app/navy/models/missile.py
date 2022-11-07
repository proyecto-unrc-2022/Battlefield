from sqlalchemy.orm import relationship

from app import db


class Missile(db.Model):
    __tablename__ = "missiles"

    id = db.Column(db.Integer, primary_key=True)
    speed = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    course = db.Column(db.String(2))
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    ship_id = db.Column(db.Integer, db.ForeignKey("ships.id"))
    navy_game_id = db.Column(
        db.Integer, db.ForeignKey("navy_games.id", ondelete="CASCADE")
    )
    is_alive = db.Column(db.Boolean, default=True)

    def __init__(
        self,
        speed,
        damage,
        course,
        pos_x,
        pos_y,
        ship_id,
        navy_game_id,
    ):
        self.speed = speed
        self.damage = damage
        self.course = course
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ship_id = ship_id
        self.navy_game_id = navy_game_id

    navy_game = relationship("NavyGame", back_populates="missiles")
    ship = relationship("Ship", back_populates="missiles")
