from app import db

class FloatingBodyDao:

    def __init__(self, obj):
        self.obj = obj

    def update_position(self, x_position=None, y_position=None, direction=None):
        if x_position: self.obj.x_position = x_position
        if y_position: self.obj.y_position = y_position
        if direction: self.obj.direction = direction
        db.session.commit()
    
