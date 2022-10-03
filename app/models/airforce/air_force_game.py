class AirForceGame:
    player_a = None
    player_b = None
    battlefield = None

    def __init__(self, p_a, p_b):
        self.player_a = p_a
        self.player_b = p_b
        self.battlefield = battlefield.battlefield()

    @classmethod
    def join_game(cls, new_player):
        if cls.player_a == None:
            cls.player_a = new_player
        elif cls.player_b == None:
            cls.player_b = new_player
        else:
            raise Exception("The game are full!")
        return {"player_a": cls.player_a, "player_b": cls.player_b}


class battlefield:
    listOfObject = []
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
    def add_new_plane(cls, player, flying_object, x, y, course):
        # course 1 north, 2 east, 3 south, 4 west
        if not cls.position_inside_map(x, y):
            raise Exception("Invalid position")

        if not cls.position_inside_player_field(x, y, course, player):
            raise Exception("Plane position cant be inside enemy field")

        cls.listOfObject.extend((player, flying_object, x, y, course))
        return cls.listOfObject

    @classmethod
    def add_new_projectile(cls, player, flying_object, x, y, course):

        if course == 1:
            cls.listOfObject.extend((player, flying_object, (x + 1), y, course))
            return cls.listOfObject
        elif course == 2:
            cls.listOfObject.extend((player, flying_object, x, (y + 1), course))
            return cls.listOfObject
        elif course == 3:
            cls.listOfObject.extend((player, flying_object, (x - 1), y, course))
            return cls.listOfObject

        cls.listOfObject.extend((player, flying_object, x, (y - 1), course))
        return cls.listOfObject

    @classmethod
    def move_projectile(cls, obj):

        speed = obj[1].get("speed")
        course = obj[4]

        if course == 1:
            if obj[2] + speed >= 20:
                obj.clear()
            else:
                obj[2] = obj[2] + speed
        elif course == 2:
            if obj[3] + speed >= 10:
                obj.clear()
            else:
                obj[3] = obj[3] + speed
        elif course == 3:
            if obj[2] - speed <= 0:
                obj.clear()
            else:
                obj[2] = obj[2] - speed
        else:
            if obj[3] - speed <= 0:
                obj.clear()
            else:
                obj[3] = obj[3] - speed

        cls.listOfObject = obj
        return cls.listOfObject


#    def moveObject():
#       for obj in listOfObject:
#          obj.x - obj.flying_object.getSpeed
