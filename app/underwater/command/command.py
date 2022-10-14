class Command:
    def __init__(self, player_id):
        self.__player_id = player_id

    def execute(self):
        raise NotImplementedError()

    def get_player_id(self):
        return self.__player_id
