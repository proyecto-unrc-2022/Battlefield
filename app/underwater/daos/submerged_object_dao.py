from app import db

from ..models.submerged_object import SubmergedObject


class SubmergedObjectDAO:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def get(obj_id):
        obj = (
            db.session.query(SubmergedObject)
            .where(SubmergedObject.id == obj_id)
            .one_or_none()
        )
        if not obj:
            raise ValueError("no floating body found with id %s" % obj_id)
        return SubmergedObjectDAO(obj)

    def update_position(self, x_position=None, y_position=None, direction=None):
        if x_position:
            self.obj.x_position = x_position
        if y_position:
            self.obj.y_position = y_position
        if direction:
            self.obj.direction = direction
        db.session.commit()

    def is_placed(self):
        return self.obj.x_position != None