import json

from app.navy import navy_constants


class NavyGameControl:
    def read_data(file_path):
        with open(file_path) as file:
            data = json.load(file)

        return data

    def __init__(
        self, id_game=None, ships=None, missiles=None, id_user_1=None, id_user_2=None
    ):
        self.id_game = id_game
        self.ships = ships
        self.missiles = missiles
        self.id_user_1 = id_user_1
        self.id_user_2 = id_user_2

         
