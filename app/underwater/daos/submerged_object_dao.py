from app import db

from ..models.submerged_object import SubmergedObject


class SubmergedObjectDAO:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, obj_id):
        obj = db.session.get(self.model, obj_id)
        if obj:
            db.session.add(obj)
        return obj

    def save(self, obj):
        db.session.add(obj)
        db.session.commit()


submerged_object_dao = SubmergedObjectDAO(SubmergedObject)
