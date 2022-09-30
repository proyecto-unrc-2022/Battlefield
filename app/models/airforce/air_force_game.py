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


#    def moveObject():
#       for obj in listOfObject:
#          obj.x - obj.flying_object.getSpeed
