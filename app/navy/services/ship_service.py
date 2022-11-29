from app.navy.daos.ship_dao import ship_dao
from app.navy.daos.ship_type_dao import ship_type_dao
from app.navy.models.ship import Ship
from app.navy.utils.navy_utils import utils


class ShipService:
    SHIP_NAMES = ["Destroyer", "Cruiser", "Battleship", "Corvette"]

    def create(self, name, pos_x, pos_y, course, user_id, navy_game_id):
        ship_data = ship_type_dao.get_by(name)
        new_ship = Ship(
            name,
            ship_data["hp"],
            ship_data["size"],
            ship_data["speed"],
            ship_data["visibility"],
            ship_data["missile_type_id"][0],
            pos_x,
            pos_y,
            course,
            user_id,
            navy_game_id,
        )
        return new_ship

    def add(self, data):
        ship = self.create(
            data["name"],
            data["pos_x"],
            data["pos_y"],
            data["course"],
            data["user_id"],
            data["navy_game_id"],
        )
        added_ship = ship_dao.add(ship)
        return added_ship

    def update_all(self, ships):
        ship_dao.update_all(ships)

    def load_to_board(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

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
                if not ship.is_alive:
                    return False
        return True

    def get_by_id(self, ship_id):
        return ship_dao.get_by_id(ship_id)

    def get_by(self, user_id=None, navy_game_id=None, ship_id=None):
        return ship_dao.get_by(
            user_id=user_id, navy_game_id=navy_game_id, ship_id=ship_id
        )

    def delete(self, ship):
        ship.is_alive = False

    def delete_from_board(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        if (
            navy_game_service.get_from_board(ship.navy_game_id, ship.pos_x, ship.pos_y)
            == ship
        ):
            ships_positions = self.build(ship)
            for x, y in ships_positions:
                navy_game_service.delete_from_board(ship.navy_game_id, x, y)

    def can_move_one(self, ship):
        x, y = utils.get_next_position(ship.pos_x, ship.pos_y, ship.course)
        return ship.is_alive and utils.in_of_bounds(x, y)

    def move_one(self, ship):
        ship.pos_x, ship.pos_y = utils.get_next_position(
            ship.pos_x, ship.pos_y, ship.course
        )

    def act(self, ship):
        from app.navy.services.navy_game_service import navy_game_service

        entity = navy_game_service.get_from_board(
            ship.navy_game_id, ship.pos_x, ship.pos_y
        )
        if entity:
            self.act_accordingly(ship, entity)

    def update_position(self, ship, dist):
        self.delete_from_board(ship)
        while self.can_move_one(ship) and dist > 0:
            self.move_one(ship)
            dist -= 1
            self.act(ship)

        if ship.is_alive:
            self.load_to_board(ship)

    def can_update(self, ship):
        from app.navy.services.navy_game_service import navy_game_service
        game_over = navy_game_service.is_over(ship.navy_game_id)
        return ship.is_alive and not game_over

    def turn(self, ship, new_course):
        self.delete_from_board(ship)
        ship.course = new_course
        if self.can_load_to_board(ship):
            self.load_to_board(ship)
            return True
        return False

    def attack(self, ship):
        from app.navy.services.missile_service import missile_service

        x, y = utils.get_next_position(ship.pos_x, ship.pos_y, ship.course)
        created_missile = missile_service.add(
            ship.navy_game_id, ship.id, ship.missile_type_id, ship.course, x, y
        )
        if utils.free_valid_poisition(x, y, ship.navy_game_id):
            missile_service.load_to_board(created_missile)
        else:
            missile_service.act_accordingly(created_missile)

    def act_accordingly(self, ship, entity):
        from app.navy.models.missile import Missile

        if isinstance(entity, Ship):
            self.act_accordingly_to_ship(ship, entity)
        elif isinstance(entity, Missile):
            self.act_accordingly_to_missile(ship, entity)

    def act_accordingly_to_ship(self, ship, other_ship):
        old_hp = ship.hp
        self.hit(ship, other_ship.hp)
        self.hit(other_ship, old_hp)

    def hit(self, ship, damage):
        self.update_hp(ship, damage)
        if self.can_delete(ship):
            self.delete(ship)
            self.delete_from_board(ship)

    def update_hp(self, ship, damage):
        ship.hp -= damage

    def can_delete(self, ship):
        return self.can_update(ship) and ship.hp <= 0

    def act_accordingly_to_missile(self, ship, missile):
        from app.navy.services.missile_service import missile_service

        self.hit(ship, missile.damage)
        missile_service.hit(missile)

    def build(self, ship):
        res = [(ship.pos_x, ship.pos_y)]
        x, y = ship.pos_x, ship.pos_y
        for _ in range(utils.ONE, ship.size):
            x, y = utils.get_next_position(x, y, utils.INVERSE_COORDS[ship.course])
            if not utils.out_of_bounds(x, y):
                res.append((x, y))
        return res

    def get_dto(self, ship):
        from app.navy.dtos.ship_dto import ShipDTO

        return ShipDTO().dump(ship)

    def pos_in_range(self, ship, pos):
        pos_x, pos_y = pos[0], pos[1]
        return utils.in_range(ship.pos_x, ship.pos_y, pos_x, pos_y, ship.visibility)

    def get_alives(self, user_id, navy_game_id):
        from app.navy.services.navy_game_service import navy_game_service

        ships = navy_game_service.get_ships(navy_game_id=navy_game_id)
        return [ship for ship in ships if ship.user_id == user_id and ship.is_alive]


ship_service = ShipService()