from app import db
from sqlalchemy.orm import relationship
from app.models.user import User


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    id_user_1 = db.Column(db.Integer, db.ForeignKey(User.id))
    id_user_2 = db.Column(db.Integer, db.ForeignKey(User.id))

    user_1 = relationship("User", foreign_keys=[id_user_1])
    user_2 = relationship("User", foreign_keys=[id_user_2])

    def __init__(self, id_user_1=None, id_user_2=None):
        self.id_user_1 = id_user_1
        self.id_user_2 = id_user_2



class DynamicShip(db.Model):
    __tablename__ = "dynamic_ships"

    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey(Game.id))
    id_user = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)
    hp = db.Column(db.Integer)
    direction = db.Column(db.String(2))
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    ship_type = db.Column(db.Integer)
    
    game = relationship("Game", back_populates="dynamic_ships")
    user = relationship("User", back_populates="dynamic_ships")

    def __init__(self, id_game, id_user, hp, direction, pos_x, pos_y, ship_type):    
        self.id_game = id_game
        self.id_user = id_user
        self.hp = hp
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ship_type = ship_type



class DynamicMissile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey(Game.id))
    id_ship = db.Column(db.Integer, db.ForeignKey(DynamicShip.id))
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    order = db.Column(db.Integer)
    direction = db.Column(db.String(2))
    missile_type = db.Column(db.Integer)

    game = relationship("Game", back_populates="dynamic_missiles")
    ship = relationship("DynamicShip", back_populates="dynamic_missiles")

    def __init__(self, id_game, id_ship, pos_x, pos_y, order, direction, missile_type):
        self.id_game = id_game
        self.id_ship = id_ship
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.order = order
        self.direction = direction
        self.missile_type = missile_type
    
