from app import db

from ...models.infantry.entity import Entity

def  add_entity(entity_id):
    succes = True
    if("1" == entity_id):
        soldier = Entity(hp=10, velocidad=3)
        db.session.add(soldier)
        db.session.commit()
    elif("2" == entity_id):
        humvee = Entity(hp=20, velocidad=5)
        db.session.add(humvee)
        db.session.commit()
    else:
        succes = False
    return succes
