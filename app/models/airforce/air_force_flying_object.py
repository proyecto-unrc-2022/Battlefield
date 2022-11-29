class FlyingObject:
    player = None
    flying_obj = None
    x: int = -1
    y: int = -1
    course = -1  # course 1 north, 2 east, 3 south, 4 west

    def __init__(self, player, flying_obj, x, y, course):
        self.player = player
        self.flying_obj = flying_obj
        self.x = x
        self.y = y
        self.course = course

    def check_invalid_course(self, course):
        return abs(self.course - course) == 2

    def update_position(
        self, course, max_x, max_y
    ):  # return true if the onbject colision with a limit
        if self.check_invalid_course(course):
            raise ValueError("New course cant be 180 degrees deference")
        self.course = course
        if course == 1:
            self.y = self.y + self.flying_obj.speed
            if self.y > max_y:
                self.y = max_y
                return True
        elif course == 2:
            self.x = self.x + self.flying_obj.speed
            if self.x > max_x:
                self.x = max_x
                return True
        elif course == 3:
            self.y = self.y - self.flying_obj.speed
            if self.y < 0:
                self.y = 0
                return True
        elif course == 4:
            self.x = self.x - self.flying_obj.speed
            if self.x < 0:
                self.x = 0
                return True
        return False

    def to_dict(self):
        return {
            "player": self.player,
            "flying_obj": self.flying_obj.id,
            "x": self.x,
            "y": self.y,
            "course": self.course,
            "flying_obj_class": self.flying_obj.__class__.__name__,
        }
