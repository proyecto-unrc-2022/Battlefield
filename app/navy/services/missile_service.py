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

    # region: Class constants
    MISSILE_TYPES = [1, 2, 3, 4]
    # endregion

    # region: Missile's Logic Methods for BD
    def get(self, navy_game_id):
        missiles = missile_dao.get_by_navy_game_id(navy_game_id)
        return missiles.sort(key=lambda x: x.order)

    def delete(self, missile):
        missile_dao.delete(missile)

    def create(self, navy_game_id, ship_id, missile_type, course, pos_x, pos_y):
        from app.navy.daos.missile_dao import missile_dao
        from app.navy.daos.missile_type_dao import missile_type_dao

        # region: 1. Create the missile
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

        # endregion
        # region: 2. Add the missile to the DB
        missile_dao.add_or_update(missile)
        # endregion
        self.add_in_map(missile)
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

    def add_in_map(self, missile):
        navy_game_service.add_in_map(
            missile.navy_game_id, missile.pos_x, missile.pos_y, missile
        )

    # endregion

    def delete_from_map(self, missile):
        navy_game_service.delete_from_map(
            missile.navy_game_id, missile.pos_x, missile.pos_y
        )

    # region: Act Accordingly
    def act_accordingly(self, missile, x_conflict, y_conflict):
        # generic act, independent of the type of entity
        navy_game_service.delete_from_map(
            missile.navy_game_id, missile.pos_x, missile.pos_y
        )
        self.delete(missile)

        if utils.is_out_of_bounds(x_conflict, y_conflict):
            return

        entity = navy_game_service.get_from_map(
            missile.navy_game_id, x_conflict, y_conflict
        )

        # En este punto se que entity tiene que ser un objeto, ya que si no, no habria conflicto
        if isinstance(entity, Missile):
            self.act_accordingly_missile(entity)
        elif isinstance(entity, Ship):
            self.act_accordingly_ship(missile, entity)

    def act_accordingly_missile(self, other_missile):
        # -- 1. Delete the missiles from the memory map -- #
        navy_game_service.delete_from_map(
            other_missile.navy_game_id, other_missile.pos_x, other_missile.pos_y
        )

        # -- 2. Delete the missiles from the DB -- #
        self.delete(other_missile)

    def act_accordingly_ship(self, missile, ship):
        from app.navy.services.ship_service import ship_service

        ship_service.update_hp(ship, missile.damage)

    # endregion

    def move(self, missile):
        old_x, old_y = missile.pos_x, missile.pos_y
        # region: 1. Move the missile
        x, y = old_x, old_y
        for _ in range(missile.speed):
            x, y = utils.get_next_position(x, y, missile.course)
            if not utils.free_valid_poisition(missile.navy_game_id, x, y):
                self.act_accordingly(missile, x, y)
                return False
            missile.pos_x, missile.pos_y = x, y
        # endregion
        # region: 2. Update the missile in the DB ( if it has moved correctly)
        else:
            navy_game_service.delete_from_map(missile.navy_game_id, old_x, old_y)
            navy_game_service.add_to_map(
                missile.navy_game_id, missile.pos_x, missile.pos_y
            )
            missile_dao.add_or_update(missile)
        # endregion
        return True

    # endregion


missile_service = MissileService()
