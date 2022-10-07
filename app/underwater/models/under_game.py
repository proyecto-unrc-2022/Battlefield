from app import db
from app.models.user import User
from sqlalchemy.orm import relationship

class UnderGame(db.Model):
    __tablename__ = "under_game"
    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    host = relationship("User", backref="under_game_h", foreign_keys=[host_id])
    visitor = relationship("User", backref="under_game_v", foreign_keys=[visitor_id])

    submerged_objects= relationship("SubmergedObject", back_populates="game")
    
    # submarines = relationship("Submarine", back_populates="game")
    # torpedos = relationship("Torpedo", back_populates="game")