from sqlalchemy import event
from sqlalchemy.orm import relationship

from app import db


class NavyGame(db.Model):

    __tablename__ = "navy_games"

    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    cols = db.Column(db.Integer)
    turn = db.Column(db.Integer)
    round = db.Column(db.Integer, default=1)
    winner = db.Column(db.Integer)
    status = db.Column(db.String(), default="WAITING_PLAYERS")
    user1_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_1 = relationship("User", foreign_keys=[user1_id])
    user_2 = relationship("User", foreign_keys=[user2_id])
    ships = relationship("Ship", back_populates="navy_game", cascade="all, delete")
    missiles = relationship(
        "Missile", back_populates="navy_game", cascade="all, delete"
    )

    def __init__(self, rows, cols, user1_id, user2_id=None):
        self.cols = cols
        self.rows = rows
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.turn = self.user1_id


@event.listens_for(NavyGame, "before_update")
def change_status(mapper, connection, target):
    from app.navy.utils.navy_game_statuses import WAITING_PICKS, WAITING_PLAYERS

    if target.status == WAITING_PLAYERS and target.user2_id:
        target.status = WAITING_PICKS
