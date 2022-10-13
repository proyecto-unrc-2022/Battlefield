from app.daos.navy.dynamic_ship_dao import delete_ship
from app.navy.daos.ship_dao import ship_dao
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.models.ship import Ship


class ShipService:
    SHIP_NAMES = ["Destroyer", "Cruiser", "Battleship", "Corvette"]

    def validate_request(self, request):
        from app.navy.validators.ship_request_validator import ShipRequestValidator

        ship_data_validated = ShipRequestValidator().load(request)
        return ship_data_validated

    def add(self, data):
        ship_data = ship_type_dao.get_by(data["name"])
        new_ship = Ship(
            data["name"],
            ship_data["hp"],
            ship_data["size"],
            ship_data["speed"],
            ship_data["visibility"],
            ship_data["missile_type_id"],
            data["pos_x"],
            data["pos_y"],
            data["course"],
            data["user_id"],
            data["navy_game_id"],
        )

        ship_dao.add_or_update(new_ship)
        return new_ship

    def get(self, navy_game_id):
        ships = ship_dao.get_by(navy_game_id=navy_game_id)
        return ships

    def delete(self, ship):
        ship_dao.delete(ship)

    def move(self, ship):
        pass

    def attack(self, ship):
        pass

    def update_hp(self, ship, damage):
        pass

    def re_build(self, ship):
        from app.navy.utils.navy_utils import utils

        res = []
        for _ in range(utils.ONE, ship.size):
            x, y = utils.get_next_position(x, y, utils.INVERSE_COORDS[ship.course])
            res.append((x, y))
        return res


ship_service = ShipService()
