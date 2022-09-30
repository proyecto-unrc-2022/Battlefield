from app import db
from app.models.user import Profile
from ...models.infantry.infantry_game import Figure_infantry
from ...models.infantry.infantry_game import Game_Infantry

def  add_entity(entity_id):
    succes = True
    if("1" == entity_id):
        soldier = Figure_infantry(hp=10, velocidad=3, tamaño=1, direccion=0,pos_x=0, pos_y=0, type=1)
        db.session.add(soldier)
        db.session.commit()
    elif("2" == entity_id):
        humvee = Figure_infantry(hp=20, velocidad=5, tamaño=2, direccion=0, pos_x=0, pos_y=0, type=2)
        db.session.add(humvee)
        db.session.commit()
    elif("3" == entity_id):
        tank = Figure_infantry(hp=50, velocidad=2, tamaño=3, direccion=0, pos_x=0, pos_y=0, type=3)
        db.session.add(tank)
        db.session.commit()
    elif("4" == entity_id):
        artillery = Figure_infantry(hp=80, velocidad=1, tamaño=4, direccion=0,pos_x=0, pos_y=0, type=4)
        db.session.add(artillery)
        db.session.commit()
    else:
        succes = False
    return succes
