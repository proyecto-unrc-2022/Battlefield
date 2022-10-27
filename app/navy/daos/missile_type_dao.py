import json


class MissileTypeDao:
    PATH_TO_MISSILE_TYPES = "app/navy/missile_types.json"

    def __init__(self) -> None:
        self.MISSILE_TYPES = self.load_data()

    def load_data(self):
        with open(self.PATH_TO_MISSILE_TYPES) as file:
            data = json.load(file)
        return data

    def get_by_id(self, id):
        return self.MISSILE_TYPES[id]


missile_type_dao = MissileTypeDao()
