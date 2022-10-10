from app import db
from sqlalchemy import or_
from app.navy.models.navy_game import NavyGame

class NavyGameDao:

  def __init__(self, model):
        self.model = model  

  def add_or_update(self, navy_game):
    db.session.add(navy_game)
    db.session.commit()

  def get(self):
    return db.session.execute(db.select(self.model)).all()

  def get_by(self, navy_game_id=None, user_id=None):
    if user_id:
      return db.session.execute(db.select(self.model).filter(or_(self.model.user1_id == user_id, self.model.user2_id == user_id))).all()
    
    return db.session.execute(db.select(self.model).filter_by(id=navy_game_id)).first()

  def delete(self, navy_game):
    db.session.delete(navy_game)
    db.session.commit()

navy_game_dao = NavyGameDao(NavyGame)
