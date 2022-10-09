from sqlalchemy.orm import relationship

from app import db
from app.underwater.game_state import GameState


class SubmergedObject(db.Model):
    __tablename__ = "submerged_object"
    id = db.Column(db.Integer, primary_key=True)
    x_position = db.Column(db.Integer)
    y_position = db.Column(db.Integer)
    direction = db.Column(db.Integer, db.CheckConstraint("direction between 0 and 7"))
    size = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))

    game_id = db.Column(db.Integer, db.ForeignKey("under_game.id"))
    game = relationship("UnderGame", back_populates="submerged_objects")

    player_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    player = relationship("User", backref="submerged_object")

    __mapper_args__ = {
        "polymorphic_identity": "submerged_object",
        "polymorphic_on": type,
    }

    def set_position(self, x_position=None, y_position=None, direction=None):
        if x_position is not None:  # Needed for when direction=0 (evaluates to False)
            self.x_position = x_position
        if y_position is not None:
            self.y_position = y_position
        if direction is not None:
            self.direction = direction

    def get_positions(self, direction=None):
        if direction is None:
            direction = self.direction
        x = self.x_position
        y = self.y_position
        i = self.size
        d = direction
        positions = []

        while i > 0:
            positions.append((x, y))
            x, y = self.move_pointer(x, y, d + 4)
            i = i - 1

        return positions

    def get_tail_positions(self, direction=None):
        if direction is None:
            direction = self.direction
        return self.get_positions(direction)[1:]

    def get_next_position(self):
        return SubmergedObject.move_pointer(
            self.x_position, self.y_position, self.direction
        )

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

    def is_placed(self):
        return self.x_position != None

    def get_game(self):
        return self.game

    def advance(self, n):
        if n > self.speed:
            raise Exception("Speed (%s) exceeded" % self.speed)

        while n > 0 and self.game.state == GameState.ONGOING:
            self.game.advance_object_one(self)
            n -= 1
