import json
from app.navy.navy_constants import PATH_TO_SHIP_TYPES

class ShipTypeDAO:

    def __init__(self) -> None:
        self.SHIP_TYPES = self.load_data()

    def load_data(self):
        with open(PATH_TO_SHIP_TYPES) as file:
            data = json.load(file)
        return data

    def get_by(self,name=None,id=None):
        for ship in self.SHIP_TYPES:
            return ship if ship["name"] == name or ship["id"] == id else None


ship_type_dao = ShipTypeDAO()


