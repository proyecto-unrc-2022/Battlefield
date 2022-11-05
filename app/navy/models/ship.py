from sqlalchemy.orm import relationship

from app import db


class Ship(db.Model):
    __tablename__ = "ships"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.Integer, nullable=False)
    missile_type_id = db.Column(db.Integer, nullable=False)

    pos_x = db.Column(db.Integer, nullable=False)
    pos_y = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(2), nullable=False)
    is_alive = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    navy_game_id = db.Column(db.Integer, db.ForeignKey("navy_games.id"))

    navy_game = relationship("NavyGame", back_populates="ships")
    missiles = relationship("Missile", back_populates="ship")
    user = relationship("User", backref="ships")

    def __init__(
        self,
        name,
        hp,
        size,
        speed,
        visibility,
        missile_type_id,
        pos_x,
        pos_y,
        course,
        user_id,
        navy_game_id,
    ):
        self.name = name
        self.hp = hp
        self.size = size
        self.speed = speed
        self.visibility = visibility
        self.missile_type_id = missile_type_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.course = course
        self.user_id = user_id
        self.navy_game_id = navy_game_id
