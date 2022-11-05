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
        missiles.sort(key=lambda x: x.order)
        return missiles

    def create(self, navy_game_id, ship_id, missile_type, course, pos_x, pos_y):
        from app.navy.daos.missile_dao import missile_dao
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
            self.get_prox_order(navy_game_id),
        )
        navy_game_service.games[navy_game_id]["missiles"].append(missile)
        return missile

    def get_prox_order(self, navy_game_id):
        return self.max_by_order(missile_dao.get_by_navy_game_id(navy_game_id)) + 1

    def max_by_order(self, missiles):
        if not missiles:
            return 0
        temp = missiles[0].order
        for m in missiles[1:]:
            temp = max(m.order, temp)
        return temp

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

    def act_accordingly(self, missile, x_conflict, y_conflict):
        self.delete(missile)

        if not utils.out_of_bounds(x_conflict, y_conflict):

            entity = navy_game_service.get_from_board(
                missile.navy_game_id, x_conflict, y_conflict
            )

            if isinstance(entity, Missile):
                self.act_accordingly_missile(entity)
            elif isinstance(entity, Ship):
                self.act_accordingly_ship(missile, entity)

    def act_accordingly_missile(self, other_missile):
        navy_game_service.delete_from_board(
            other_missile.navy_game_id, other_missile.pos_x, other_missile.pos_y
        )
        self.delete(other_missile)

    def act_accordingly_ship(self, missile, ship):
        from app.navy.services.ship_service import ship_service

        ship_service.update_hp(ship, missile.damage)

    def update_position(self, missile):
        self.delete_from_board(missile)

        for _ in range(missile.speed):

            new_position = utils.next_free_position(
                missile.pos_x, missile.pos_y, missile.course, missile.navy_game_id
            )
            if new_position:
                missile.pos_x, missile.pos_y = new_position
                continue
            x_conflict, y_conflit = utils.get_next_position(
                x=missile.pos_x, y=missile.pos_y, course=missile.course
            )
            self.act_accordingly(missile, x_conflict, y_conflit)
            return False

        navy_game_service.load_to_board(
            missile.navy_game_id, missile.pos_x, missile.pos_y, missile
        )

        return True

    def get_dto(self, missile):
        from app.navy.dtos.missile_dto import MissileDTO

        return MissileDTO().dump(missile)


missile_service = MissileService()
