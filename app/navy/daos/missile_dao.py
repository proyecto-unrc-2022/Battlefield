from app import db
from app.navy.models.missile import Missile


class MissileDAO:

    def __init__(self, model):
        self.model = model

    def add_or_update(self,missile):
        db.session.add(missile)
        db.session.commit()
        #return missile 

    def get_missile_by_id(self,id):
        return db.session.query(self.model).filter_by(id=id).first()

    def get_missiles_by(self,id_missile=None, id_ship=None, id_navy_game=None):
        return db.session.query(self.model).filter_by(id=id_missile, ship_id=id_ship, navy_game_id=id_navy_game).first()

    def delete_missile(self,missile):
        db.session.delete(missile)
        db.session.commit()
    
    def get_missiles_by_navy_game_id(self, navy_game_id):
        return db.session.query(self.model).filter_by(navy_game_id=navy_game_id).all()

missile_dao = MissileDAO(Missile)