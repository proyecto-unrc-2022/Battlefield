from app.navy.daos.ship_dao import ship_dao
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.models.ship import Ship
from app.navy.utils.navy_utils import utils


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

    def is_alive(self, ship_id):
        return ship_dao.get_by_id(ship_id)

    def get_by(self, user_id=None, navy_game_id=None, ship_id=None):
        return ship_dao.get_by(
            user_id=user_id, navy_game_id=navy_game_id, ship_id=ship_id
        )

    def delete(self, ship):
        ship_dao.delete(ship)

    def turn(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        new_positions = self.build(ship)

        for x, y in new_positions[1:]:
            entity = navy_game_service.get_from_map(ship.navy_game_id, x, y)
            if entity:
                self.act_accordingly(ship, entity)
                if not self.is_alive(ship.id):
                    return False

        ship_dao.add_or_update(ship)
        return True

    def act_accordingly(self, ship, entity):
        from app.navy.models.missile import Missile

        if isinstance(entity, Ship):
            self.act_accordingly_to_ship(ship, entity)

        if isinstance(entity, Missile):
            self.act_accordingly_to_missile(ship, entity)

    def act_accordingly_to_ship(self, ship, other_ship):
        self.update_hp(ship, other_ship.hp)
        self.update_hp(other_ship, ship.hp)

    def act_accordingly_to_missile(self, ship, missile):
        from app.navy.services.missile_service import missile_service

        self.update_hp(ship, missile.damage)
        missile_service.delete_from_map(missile)
        missile_service.delete(missile)

    def move(self, ship, action):
        from app.navy.services.navy_game_service import navy_game_service

        old_positions = self.build(ship)
        for _ in range(action.move):
            x, y = utils.get_next_position(ship.pos_x, ship.pos_y, ship.course)
            if utils.is_out_of_bounds(x, y):
                ship_dao.add_or_update(ship)
                break
            entity = navy_game_service.get_from_map(ship.navy_game_id, x, y)
            if entity:
                self.act_accordingly(ship, entity)
                break
            ship.pos_x, ship.pos_y = x, y
        else:
            ship_dao.add_or_update(ship)
            self.delete_from_map(ship)
            for x, y in self.build(ship):
                navy_game_service.add_in_map(ship.navy_game_id, x, y)
            return True

        return False

    def attack(self, ship):
        from app.navy.services.missile_service import missile_service

        x, y = utils.get_next_position(ship.pos_x, ship.pos_y)
        created_missile = missile_service.create(
            ship.navy_game_id, ship.id, ship.missile_type_id, ship.course, x, y
        )
        if not utils.free_valid_poisition(ship.navy_game_id, ship.pos_x, ship.pos_y):
            missile_service.act_accordingly(created_missile, x, y)
            return False
        return True

    def delete_from_map(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        ships_positions = self.build(ship)
        for x, y in ships_positions:
            navy_game_service.delete_from_map(ship.navy_game_id, x, y)

    def update_hp(self, ship, damage):
        if ship.hp - damage <= utils.ZERO:
            self.delete(ship)
            self.delete_from_map(ship)

        ship.hp -= damage
        ship_dao.add_or_update(ship)

    def build(self, ship):
        res = [(ship.x, ship.y)]
        for _ in range(utils.ONE, ship.size):
            x, y = utils.get_next_position(x, y, utils.INVERSE_COORDS[ship.course])
            res.append((x, y))
        return res


ship_service = ShipService()
