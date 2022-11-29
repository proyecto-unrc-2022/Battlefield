from sqlalchemy import event
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


@event.listens_for(Ship, "after_insert")
def ship_change(mapper, connection, target):
    from app.navy.models.navy_game import NavyGame

    navy_game = db.session.query(NavyGame).filter_by(id=target.navy_game_id).first()

    user_1 = navy_game.user1_id
    user_2 = navy_game.user2_id

    ships_user1 = (
        db.session.query(Ship)
        .filter_by(navy_game_id=target.navy_game_id, user_id=user_1)
        .all()
    )

    ships_user2 = (
        db.session.query(Ship)
        .filter_by(navy_game_id=target.navy_game_id, user_id=user_2)
        .all()
    )

    if ships_user1 and ships_user2:
        from app.navy.utils.navy_game_statuses import STARTED

        connection.execute(
            f'UPDATE navy_games SET status = "{STARTED}" WHERE id = {target.navy_game_id}'
        )
