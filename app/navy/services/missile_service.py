from app.navy.daos.missile_dao import missile_dao
from app.navy.models.missile import Missile
from app.navy.models.ship import Ship
from app.navy.services.navy_game_service import navy_game_service
from app.navy.utils.navy_utils import utils

""" Missile Service

    This class is responsible for the logic of the missiles in the game.
    It is responsible for the creation of missiles, the movement of missiles, the attack of missiles,the deletion of missiles, etc.
    
    Attributes:
        MISSILE_TYPES (list): List of missile types.

    Methods:
        add(self,navy_Game_id,ship_id,missile_type,pos_x,pos_y)
        get(self,navy_game_id)
        delete(self,missile)
        move(self,missile)
        mov_is_valid(self,missile,x,y)
        act_accordingly(self,missile,x,y)
           |-> act_accordingly_missile(self,other_missile)
           |-> act_accordingly_ship(self,damage,ship)
        
    You can view in github the source code of this class:
    missile_service: https://github.com/proyecto-unrc-2022/Battlefield/tree/develop/app/navy
    
"""


class MissileService:

    MISSILE_TYPES = [1, 2, 3, 4]

    def get(self, navy_game_id):
        missiles = missile_dao.get_by_navy_game_id(navy_game_id=navy_game_id)
        return missiles

    def create(self, navy_game_id, ship_id, missile_type, course, pos_x, pos_y):
        from app.navy.daos.missile_type_dao import missile_type_dao

        missile_data = missile_type_dao.get_by_id(str(missile_type))
        missile = Missile(
            missile_data["speed"],
            missile_data["damage"],
            course,
            pos_x,
            pos_y,
            ship_id,
            navy_game_id,
        )
        navy_game_service.games[navy_game_id]["missiles"].append(missile)
        return missile

    def update_db(self, missile):
        missile_dao.add_or_update(missile)

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

    def can_update(f):
        def prepare_update(self, missile):
            game_over = navy_game_service.is_game_over(missile.navy_game_id)
            if missile.is_alive and not game_over:
                speed = missile.speed
                f(self, missile)
                missile.speed = speed

        return prepare_update

    def can_move_one(self, missile):
        x, y = utils.get_next_position(missile.pos_x, missile.pos_y, missile.course)
        return missile.is_alive and missile.speed > 0

    def move_one(self, missile):
        missile.pos_x, missile.pos_y = utils.get_next_position(
            missile.pos_x, missile.pos_y, missile.course
        )
        missile.speed -= 1
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
        while self.can_move_one(missile):
            self.move_one(missile)
            self.act(missile)

        if missile.is_alive:
            self.load_to_board(missile)

    def get_dto(self, missile):
        from app.navy.dtos.missile_dto import MissileDTO

        return MissileDTO().dump(missile)


missile_service = MissileService()
