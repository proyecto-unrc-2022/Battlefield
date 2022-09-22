from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.orm import relationship #investigar


from app import db
from app.models.user import User

class Game_Infantry(db.model):

    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    id_player1 = db.Column(db.Integer, db.ForeignKey("users.id"))
    id_player2 = db.Column(db.Integer, db.ForeignKey("users.id"))


class figure_infantry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("User.id"), unique=True)
    #id_proyectil = db.Column(db.Integer, unique=True) Sacar!
    #id_game = db.Column(db.Integer, db.ForeignKey(""), unique=True)
    #hp = db.Column(db.Integer, nullable=False)
    #velocidad = db.Column(db.Integer, nullable=False)
    #tamaño = db.Column(db.Integer, nullable=False)
    #direccion = db.Column(db.String(2), nullable=False)
    #pos_x = db.Column(db.Integer, nullable=False)
    #pos_y = db.Column(db.Integer, nullable=False)
    

    #def __init__(self, id_user,id_game, hp, velocidad, tamaño, direccion, pos_x, pos_y):


class Projectile(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    #id_game = db.Column(db.Integer, db.ForeignKey(""), unique=True)
    #pos_x = db.Column(db.Integer, nullable=False)
    #pos_y = db.Column(db.Integer, nullable=False)
    #duracion = db.Column(db.Integer, nullable=False)
    #daño = db.Column(db.Integer, nullable=False)
    #direccion = db.Column(db.String(2), nullable=False)

    #def __init__(self,)






#class Personaje(db.Model):



#class Artillería(db.Model):
    

#class Tanque(db.Model):


#class Humvee(db.Model):


#class Soldado(db.Model):
