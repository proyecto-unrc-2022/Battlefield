from app import db
from app.underwater.models import SubmergedObject


class SubmergedObjectDAO:
    def get_by_id(self, obj_id):
        return db.session.get(SubmergedObject, obj_id)

    def save(self, obj):
        db.session.add(obj)
        db.session.commit()


submerged_object_dao = SubmergedObjectDAO()
