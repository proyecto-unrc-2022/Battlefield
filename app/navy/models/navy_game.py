from sqlalchemy.orm import relationship

from app import db


class NavyGame(db.Model):

    __tablename__ = "navy_games"

    id = db.Column(db.Integer, primary_key=True)
    board_rows = db.Column(db.Integer)
    board_colums = db.Column(db.Integer)
    turn = db.Column(db.Integer)
    round = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    user1_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user_1 = relationship("User", foreign_keys=[user1_id])
    user_2 = relationship("User", foreign_keys=[user2_id])
    ships = relationship("Ship", back_populates="navy_game", cascade="all, delete")
    missiles = relationship(
        "Missile", back_populates="navy_game", cascade="all, delete"
    )

    def __init__(self, board_rows, board_colums, user1_id, user2_id=None):
        self.board_colums = board_colums
        self.board_rows = board_rows
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.turn = self.user1_id
        self.round = 1
        self.user1_played = False
        self.user2_played = False

