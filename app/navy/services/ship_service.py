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
            ship_data["missile_type_id"][0],
            data["pos_x"],
            data["pos_y"],
            data["course"],
            data["user_id"],
            data["navy_game_id"],
        )

        ship_dao.add_or_update(new_ship)
        return new_ship

    def get_by_id(self, ship_id):
        return ship_dao.get_by_id(ship_id)

    def get_by(self, user_id=None, navy_game_id=None, ship_id=None):
        return ship_dao.get_by(
            user_id=user_id, navy_game_id=navy_game_id, ship_id=ship_id
        )

    def delete(self, ship):
        ship_dao.delete(ship)

    def move(self, ship):
        pass

    def attack(self, ship):
        pass

    def delete_in_map(self, ship):
        from app.navy.services.navy_game_service import navy_game_service
        ships_positions = self.build(ship)
        for x,y in ships_positions:
            navy_game_service.delete_in_map(ship.navy_game_id,x,y)

    def update_hp(self, ship, damage):
        from app.navy.utils.navy_utils import utils #Todo navyutils twice
        if ship.hp - damage <= utils.ZERO:
            self.delete(ship)
            self.delete_in_map(ship)
        
        ship.hp -= damage
        ship_dao.add_or_update(ship)
   

    def build(self, ship):
        from app.navy.utils.navy_utils import utils

        res = [(ship.x,ship.y)]
        for _ in range(utils.ONE, ship.size):
            x, y = utils.get_next_position(x, y, utils.INVERSE_COORDS[ship.course])
            res.append((x, y))
        return res


ship_service = ShipService()
