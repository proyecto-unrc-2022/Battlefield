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

    @classmethod
    def addNewObject(cls, player, flying_object, x, y, course):
        global listOfObject
        cls.listOfObject.extend((player, flying_object, x, y, course))
        return cls.listOfObject


#    def moveObject():
#       for obj in listOfObject:
#          obj.x - obj.flying_object.getSpeed
