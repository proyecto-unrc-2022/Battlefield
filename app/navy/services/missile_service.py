from app.navy.daos.missile_dao import missile_dao
from app.navy.models.missile import Missile
from app.navy.models.ship import Ship
from app.navy.services.navy_game_service import navy_game_service
from app.navy.utils.navy_utils import utils


class MissileService:
    def get(self, navy_game_id):
        missiles = missile_dao.get_by_navy_game_id(navy_game_id=navy_game_id)
        return missiles

    def create(self, navy_game_id, pos_x, pos_y, course, missile_type, ship_id):
        from app.navy.daos.missile_type_dao import missile_type_dao

        missile_data = missile_type_dao.get_by_id(str(missile_type))
        new_missile = Missile(
            missile_data["speed"],
            missile_data["damage"],
            course,
            pos_x,
            pos_y,
            ship_id,
            navy_game_id,
        )
        return new_missile

    def add(self, navy_game_id, ship_id, missile_type, course, pos_x, pos_y):
        new_missile = self.create(
            navy_game_id, pos_x, pos_y, course, missile_type, ship_id
        )
        navy_game_service.games[navy_game_id]["missiles"].append(new_missile)
        return new_missile

    def update_all(self, missiles):
        missile_dao.update_all(missiles)

    def load_to_board(self, missile):
        navy_game_service.load_to_board(
            missile.navy_game_id, missile.pos_x, missile.pos_y, missile
        )

    def delete_from_board(self, missile):
        navy_game_service.delete_from_board(
            missile.navy_game_id, missile.pos_x, missile.pos_y
        )

    def get_alives(self, navy_game_id):
        all_missiles = navy_game_service.get_missiles(navy_game_id)
        return list(filter(lambda x: x.is_alive, all_missiles))

    def delete(self, missile):
        missile.is_alive = False

    def act_accordingly(self, missile):
        from app.navy.services.ship_service import ship_service

        self.delete(missile)
        entity = navy_game_service.get_from_board(
            missile.navy_game_id, missile.pos_x, missile.pos_y
        )

        if isinstance(entity, Missile):
            self.hit(entity)
        elif isinstance(entity, Ship):
            ship_service.hit(entity, missile.damage)

    def hit(self, missile):
        self.delete_from_board(missile)
        self.delete(missile)

    def can_update(update_position):
        def prepare_update(self, missile):
            game_over = navy_game_service.is_over(missile.navy_game_id)
            if missile.is_alive and not game_over:
                update_position(self, missile)

        return prepare_update

    def can_move_one(self, missile):
        return missile.is_alive

    def move_one(self, missile):
        missile.pos_x, missile.pos_y = utils.get_next_position(
            missile.pos_x, missile.pos_y, missile.course
        )
        return missile

    def act(self, missile):
        entity = navy_game_service.get_from_board(
            missile.navy_game_id, missile.pos_x, missile.pos_y
        )
        if entity or utils.out_of_bounds(missile.pos_x, missile.pos_y):
            self.act_accordingly(missile)

    @can_update
    def update_position(self, missile):
        self.delete_from_board(missile)
        dist = missile.speed
        while self.can_move_one(missile) and dist > 0:
            self.move_one(missile)
            dist -= 1
            self.act(missile)

        if missile.is_alive:
            self.load_to_board(missile)

    def get_dto(self, missile):
        from app.navy.dtos.missile_dto import MissileDTO

        return MissileDTO().dump(missile)


missile_service = MissileService()
