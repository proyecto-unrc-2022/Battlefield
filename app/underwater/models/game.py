from app import db

from sqlalchemy.orm import relationship

class UnderGame(db.Model):
    # __tablename__ = 'under_game'
    id = db.Column(db.Integer, primary_key= True)
    
    host = relationship("UserSchema", uselist=False)
    visitor = relationship("UserSchema", uselist=False)