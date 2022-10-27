from app import db

from ..models.submerged_object import SubmergedObject


class SubmergedObjectDAO:
    def __init__(self, model):
        self.model = model

    def save(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get_by_id(self, obj_id):
        sub = db.session.get(self.model, obj_id)
        if not sub:
            raise ValueError("no submerged object found with id %s" % obj_id)
        return sub


submerged_object_dao = SubmergedObjectDAO(SubmergedObject)
