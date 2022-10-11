import json


class ShipTypeDAO:
    PATH_TO_SHIP_TYPES = "app/navy/ship_types.json"

    def __init__(self) -> None:
        self.SHIP_TYPES = self.load_data()

    def load_data(self):
        with open(self.PATH_TO_SHIP_TYPES) as file:
            data = json.load(file)
        return data

    def get_by(self, name):
        return self.SHIP_TYPES[name]


ship_type_dao = ShipTypeDAO()
