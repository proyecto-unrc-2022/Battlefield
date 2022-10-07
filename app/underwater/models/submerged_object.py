from app import db
from sqlalchemy.orm import relationship

class SubmergedObject(db.Model):
    __tablename__ = "submerged_object"
    id = db.Column(db.Integer, primary_key=True)
    x_position = db.Column(db.Integer)
    y_position = db.Column(db.Integer)
    direction = db.Column(db.Integer, db.CheckConstraint("direction between 0 and 7"))
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))

    game_id = db.Column(db.Integer, db.ForeignKey("under_game.id"))
    game = relationship("UnderGame", back_populates="submerged_objects")

    player_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    player = relationship("User", backref="submerged_object")

    __mapper_args__ = {
        "polymorphic_identity": "submerged_object",
        "polymorphic_on": type
    }