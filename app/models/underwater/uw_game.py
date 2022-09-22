from sqlalchemy.orm import relationship
import json

from app import db
from app.models.user import User

class UnderGame(db.Model):
    __tablename__ = 'under_games'
    id = db.Column(db.Integer, primary_key= True)

    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(User.id))
    
    # host = relationship("User", uselist=False, back_populates='user')
    # visitor = relationship("User", uselist=False, back_populates='user')

    def __repr__(self):
        return json.dumps({"game_id":self.id, "host_id":self.host_id, "visitor_id":self.visitor_id})
