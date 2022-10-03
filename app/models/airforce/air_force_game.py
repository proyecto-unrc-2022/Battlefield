from calendar import c


class flying_object:
    player = None
    flying_obj = None
    x = -1
    y = -1
    course = -1  # course 1 north, 2 east, 3 south, 4 west

    def __init__(self, player, flying_obj, x, y, course):
        self.player = player
        self.flying_obj = flying_obj
        self.x = x
        self.y = y
        self.course = course

    @classmethod
    def check_course(self, course):
        return abs(self.course - course) == 2

    def update_position(self, course):
        if self.check_course(course):
            raise ValueError("New course cant be 180 degrees deference")
        if course == 1:
            self.y = self.y + self.flying_obj.speed
        elif course == 2:
            self.x = self.x + self.flying_obj.speed
        elif course == 3:
            self.y = self.y - self.flying_obj.speed
        elif course == 4:
            self.x = self.x - self.flying_obj.speed

    def to_dict(self):
        return {
            "player": self.player,
            "flying_obj": self.flying_obj.id,
            "x": self.x,
            "y": self.y,
            "course": self.course,
        }


class battlefield:
    flying_objects = []
    max_x = 20
    max_y = 10

    @classmethod
    def position_inside_map(cls, x, y):
        if x > cls.max_x:
            return False
        if x < 1:
            return False
        if y > cls.max_y:
            return False
        if y < 1:
            return False
        return True

    @classmethod
    def position_inside_player_field(cls, x, y, course, player):
        if AirForceGame.player_a == player:
            if x > cls.max_x / 2:
                return False
            if (x == (cls.max_x / 2)) and course != 2:
                return False
        if AirForceGame.player_b == player:
            if x <= cls.max_x / 2:
                return False
            if (x == (cls.max_x / 2) + 1) and course != 4:
                return False

        return True

    @classmethod
    def add_new_plane(cls, player, obj, x, y, course):
        if not cls.position_inside_map(x, y):
            raise Exception("Invalid position")

        if not cls.position_inside_player_field(x, y, course, player):
            raise Exception("Plane position cant be inside enemy field")

        fly_obj = flying_object(player, obj, x, y, course)
        cls.flying_objects.append(fly_obj)
        return fly_obj

    @classmethod
    def fligth(cls, player, course):
        obj = list(
            filter(
                lambda x: x.player == player
                and x.flying_obj.__class__.__name__ == "Plane",
                cls.flying_objects,
            )
        )[0]
        print(obj.flying_obj)
        obj.update_position(course)

    @classmethod
    def add_new_projectile(cls, player, obj, x, y, course):
        fly_obj = flying_object(player, obj, x, y, course)
        if course == 1:
            fly_obj.x + 1
        elif course == 2:
            fly_obj.y + 1
        elif course == 3:
            fly_obj.x - 1
        elif course == 4:
            fly_obj.y - 1
        cls.flying_objects.append(fly_obj)
        return fly_obj

    # @classmethod
    # def move_projectile(cls, player):#yo lo haria asi, total de actualizar actualizarias todos los proyectiles de un jugador de ultima en el orden de creacion

    #     speed = obj.flying_object.speed
    #     course = obj.course

    #     if course == 1:
    #         if obj.x + speed >= 20:
    #             obj.clear()
    #         else:
    #             obj.x = obj.x + speed
    #     elif course == 2:
    #         if obj.y + speed >= 10:
    #             obj.clear()
    #         else:
    #             obj.y = obj.y + speed
    #     elif course == 3:
    #         if obj.x - speed <= 0:
    #             obj.clear()
    #         else:
    #             obj.x = obj.x - speed
    #     else:
    #         if obj.y - speed <= 0:
    #             obj.clear()
    #         else:
    #             obj.y = obj.y - speed

    #     cls.flying_objects = obj
    #     return cls.flying_objects


class AirForceGame:
    player_a = None
    player_b = None
    battlefield = battlefield()

    def __init__(self, p_a, p_b):
        self.player_a = p_a
        self.player_b = p_b
        self.battlefield = battlefield()

    @classmethod
    def join_game(cls, new_player):
        if cls.player_a == None:
            cls.player_a = new_player
        elif cls.player_b == None:
            cls.player_b = new_player
        else:
            raise Exception("The game are full!")
        return {"player_a": cls.player_a, "player_b": cls.player_b}
