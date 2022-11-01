from app.navy.daos.ship_dao import ship_dao
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.models.ship import Ship
from app.navy.utils.navy_utils import utils


class ShipService:
    SHIP_NAMES = ["Destroyer", "Cruiser", "Battleship", "Corvette"]
    SHIP_SIZES = [3, 3, 4, 2]

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

        return ship_dao.add_or_update(new_ship)

    def load_to_board(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        # TODO: CanLoad to board
        ships_positions = self.build(ship)
        for x, y in ships_positions:
            navy_game_service.load_to_board(ship.navy_game_id, x, y, ship)

    def can_load_to_board(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        ships_positions = self.build(ship)
        for x, y in ships_positions:
            entity = navy_game_service.get_from_board(ship.navy_game_id, x, y)
            if entity:
                self.act_accordingly(ship, entity)
                if not self.is_alive(ship.id):
                    return False
        return True

    def get_by_id(self, ship_id):
        return ship_dao.get_by_id(ship_id)

    def get_by(self, user_id=None, navy_game_id=None, ship_id=None):
        return ship_dao.get_by(
            user_id=user_id, navy_game_id=navy_game_id, ship_id=ship_id
        )

    def delete(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        navy_game_service.delete_entity(ship)
        ship_dao.delete(ship)

    def delete_from_board(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        ships_positions = self.build(ship)
        for x, y in ships_positions:
            navy_game_service.delete_from_board(ship.navy_game_id, x, y)

    def update_position(self, ship, action):
        from app.navy.services.navy_game_service import navy_game_service

        self.delete_from_board(ship)
        for _ in range(int(action.move)):
            x, y = utils.get_next_position(ship.pos_x, ship.pos_y, ship.course)
            if utils.out_of_bounds(x, y):
                self.load_to_board(ship)
                ship_dao.add_or_update(ship)
                return True

            entity = navy_game_service.get_from_board(ship.navy_game_id, x, y)
            if entity:
                self.act_accordingly(ship, entity)
                if not self.is_alive(ship.id):
                    return False
            ship.pos_x, ship.pos_y = x, y

        ship_dao.add_or_update(ship)
        self.load_to_board(ship)
        return True

    def turn(self, ship, new_course):
        self.delete_from_board(ship)
        ship.course = new_course
        if self.can_load_to_board(ship):
            self.load_to_board(ship)
            ship_dao.add_or_update(ship)
            return True
        return False

    def attack(self, ship):
        from app.navy.services.missile_service import missile_service

        x, y = utils.get_next_position(ship.pos_x, ship.pos_y, ship.course)
        created_missile = missile_service.create(
            ship.navy_game_id, ship.id, ship.missile_type_id, ship.course, x, y
        )
        if not utils.free_valid_poisition(x, y, ship.navy_game_id):
            missile_service.act_accordingly(created_missile, x, y)
            return False

        missile_service.load_to_board(created_missile)
        return True

    def update_hp(self, ship, damage):
        from app.navy.services.navy_game_service import navy_game_service

        if ship.hp - damage <= utils.ZERO:
            self.delete(ship)
            if navy_game_service.get_from_board(
                ship.navy_game_id, ship.pos_x, ship.pos_y
            ):
                self.delete_from_board(ship)
        else:
            ship.hp -= damage
            ship_dao.add_or_update(ship)

    def act_accordingly(self, ship, entity):
        from app.navy.models.missile import Missile

        if isinstance(entity, Ship):
            self.act_accordingly_to_ship(ship, entity)

        if isinstance(entity, Missile):
            self.act_accordingly_to_missile(ship, entity)

    def is_alive(self, ship_id):
        return ship_dao.get_by_id(ship_id)

    def act_accordingly_to_ship(self, ship, other_ship):
        old_hp = ship.hp
        self.update_hp(ship, other_ship.hp)
        self.update_hp(other_ship, old_hp)

    def act_accordingly_to_missile(self, ship, missile):
        from app.navy.services.missile_service import missile_service

        self.update_hp(ship, missile.damage)
        missile_service.delete_from_board(missile)
        missile_service.delete(missile)

    def build(self, ship):
        res = [(ship.pos_x, ship.pos_y)]
        x, y = ship.pos_x, ship.pos_y
        for _ in range(utils.ONE, ship.size):
            x, y = utils.get_next_position(x, y, utils.INVERSE_COORDS[ship.course])
            if not utils.out_of_bounds(x, y):
                res.append((x, y))
        return res

    # -- End Private Methods -- #


ship_service = ShipService()
