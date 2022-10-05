from sqlalchemy.orm import relationship

from app import db
from app.models.user import User

class UnderGame(db.Model):
    __tablename__ = "under_game"
    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    host = relationship("User", backref="under_game_h", foreign_keys=[host_id])
    visitor = relationship("User", backref="under_game_v", foreign_keys=[visitor_id])

    submarines = relationship("Submarine", back_populates="game")
    torpedos = relationship("Torpedo", back_populates="game")

    # def __repr__(self):
    #     return json.dumps(
    #         {"game_id": self.id, "host_id": self.host_id, "visitor_id": self.visitor_id}
    #     )

class FloatingBody(db.Model):
    __tablename__ = "floating_body"
    id = db.Column(db.Integer, primary_key=True)
    x_position = db.Column(db.Integer)
    y_position = db.Column(db.Integer)
    direction = db.Column(db.Integer, db.CheckConstraint("direction between 0 and 7"))
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))

    game_id = db.Column(db.Integer, db.ForeignKey("under_game.id"))

    __mapper_args__ = {
        "polymorphic_identity": "floating_body",
        "polymorphic_on": type
    }

class Submarine(FloatingBody):
    __tablename__ = "submarine"
    id = db.Column(db.Integer, db.ForeignKey("floating_body.id"), primary_key=True)
    name = db.Column(db.String(50))
    visibility = db.Column(db.Integer, nullable=False)
    radar_scope = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Float, nullable=False)
    torpedo_speed = db.Column(db.Integer, nullable=False)
    torpedo_damage = db.Column(db.Float, nullable=False)

    game = relationship("UnderGame", back_populates="submarines")

    player_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    player = relationship("User", backref="submarine")

    __mapper_args__ = {
        "polymorphic_identity": "submarine"
    }


class Torpedo(FloatingBody):
    id = db.Column(db.Integer, db.ForeignKey("floating_body.id"), primary_key=True)
    damage = db.Column(db.Integer, nullable=False)

    game = relationship("UnderGame", back_populates="torpedos")

    __mapper_args__ = {
        "polymorphic_identity": "torpedo"
    }


class UnderBoard:
    def __init__(self, id, height=10, width=20):
        self.id = id
        self.height = height
        self.width = width
        self.matrix = []
        for i in range(height):
            self.matrix.append([None] * width)

    @staticmethod
    def move_pointer(x, y, direction):
        d = direction % 8
        if d == 0:
            return x - 1, y
        elif d == 1:
            return x - 1, y + 1
        elif d == 2:
            return x, y + 1
        elif d == 3:
            return x + 1, y + 1
        elif d == 4:
            return x + 1, y
        elif d == 5:
            return x + 1, y - 1
        elif d == 6:
            return x, y - 1
        elif d == 7:
            return x - 1, y - 1
        else:
            raise TypeError("direction must be an integer")

    def valid(self, x, y):
        return x >= 0 and x < self.height and y >= 0 and y < self.width

    def place(self, obj, x_coord, y_coord, direction, size=1):
        i = size
        x = x_coord
        y = y_coord
        d = direction

        if not self.valid(x_coord, y_coord):
            raise Exception("Invalid coordinates")

        if not self.segment_is_empty(x, y, d, i):
            raise Exception("Given position is not available")

        while i > 0 and self.valid(x, y):
            self.matrix[x][y] = obj
            x, y = self.move_pointer(x, y, d + 4)  # +4 inverts the direction
            i = i - 1

    def get_cell_content(self, x, y):
        if not self.valid(x, y):
            raise ValueError("Invalid coordinates")

        return self.matrix[x][y]

    def segment_is_empty(self, x_coord, y_coord, direction=0, length=1):
        d = direction % 8
        i = length
        x = x_coord
        y = y_coord

        while i > 0 and self.valid(x, y):
            if self.get_cell_content(x, y):
                return False
            x, y = self.move_pointer(x, y, d)
            i = i - 1

        return True


boards = {}
