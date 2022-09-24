from sqlalchemy.orm import relationship

from app import db
from app.models.user import User


class UnderGame(db.Model):
    __tablename__ = "under_games"
    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    # host = relationship("User", uselist=False, foreign_keys="user.id")
    # visitor = relationship("User", uselist=False, foreign_keys="user.id")

    submarines = relationship("Submarine", back_populates="game")
    torpedos = relationship("Torpedo", back_populates="game")

    # def __repr__(self):
    #     return json.dumps(
    #         {"game_id": self.id, "host_id": self.host_id, "visitor_id": self.visitor_id}
    #     )


class Submarine(db.Model):
    __tablename__ = "submarines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.Integer, nullable=False)
    radar_scope = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Float, nullable=False)
    torpedo_speed = db.Column(db.Integer, nullable=False)
    torpedo_damage = db.Column(db.Float, nullable=False)
    x_position = db.Column(db.Integer)
    y_position = db.Column(db.Integer)
    direction = db.Column(db.Integer, db.CheckConstraint("direction between 0 and 7"))

    game_id = db.Column(db.Integer, db.ForeignKey("under_games.id"))
    game = relationship("UnderGame", back_populates="submarines")

    player_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    player = relationship("User")


class Torpedo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speed = db.Column(db.Integer, nullable=False)
    damage = db.Column(db.Integer, nullable=False)
    x_position = db.Column(db.Integer)
    y_position = db.Column(db.Integer)
    direction = db.Column(db.Integer, db.CheckConstraint("direction between 0 and 7"))

    game_id = db.Column(db.Integer, db.ForeignKey("under_games.id"))
    game = relationship("UnderGame", back_populates="torpedos")
