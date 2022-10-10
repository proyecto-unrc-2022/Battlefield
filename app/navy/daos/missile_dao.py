from app import db
from app.navy.models.missile import Missile


class MissileDAO:

    def add_or_update(self,missile):
        db.session.add(missile)
        db.session.commit()
        #return missile 

    def get_missile_by_id(self,id):
        return db.session.execute(db.select(Missile).filter_by(id=id)).scalar_one()

    def get_missiles_by(self,id_missile=None, id_ship=None, id_navy_game=None):
        db.session.execute(db.select(Missile).filter_by(id=id_missile, ship_id=id_ship, navy_game_id=id_navy_game)).scalar_one()
    def delete_missile(self,missile):
        db.session.delete(missile)
        db.session.commit()
    
    def get_missiles_by_navy_game_id(self, navy_game_id):
        return db.session.execute(db.select(Missile).filter_by(navy_game_id=navy_game_id)).scalars().all()


missile_dao = MissileDAO(Missile)