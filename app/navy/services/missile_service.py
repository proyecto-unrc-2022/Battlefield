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

    #region: Class constants
    MISSILE_TYPES = [1, 2, 3, 4]
    #endregion

    #region: Missile's Logic Methods for BD
    def get(self, navy_game_id):
        missiles = missile_dao.get_by_navy_game_id(navy_game_id)
        return missiles.sort(key=lambda x: x.order)

    def delete(self, missile):
        missile_dao.delete(missile)

    def add(self, navy_game_id, ship_id, missile_type, course):
        #region: 1. Create the missile
        missile = Missile(navy_game_id, ship_id, missile_type, course)
        #endregion
        #region: 2. Add the missile to the DB
        missile_dao.add_or_update(missile)
        #endregion
        
        navy_game_service.add_to_map(missile.navy_game_id, missile.pos_x, missile.pos_y)

      
        
    
    #endregion

    #region: Act Accordingly
    def act_accordingly(self, missile,x_conflict,y_conflict):
        #generic act, independent of the type of entity
        navy_game_service.delete_in_map(missile.navy_game_id, missile.pos_x, missile.pos_y)
        self.delete(missile)

        if utils.is_out_of_bounds(x_conflict, y_conflict):
            return

        entity = navy_game_service.get_from_map(missile.navy_game_id, x_conflict, y_conflict)

        #En este punto se que entity tiene que ser un objeto, ya que si no, no habria conflicto
        if isinstance(entity, Missile):
            self.act_accordingly_missile(entity)
        elif isinstance(entity, Ship):
            self.act_accordingly_ship(missile,entity)

            
    def act_accordingly_missile(self,other_missile):
        #-- 1. Delete the missiles from the memory map -- #
        navy_game_service.delete_in_map(other_missile.navy_game_id, other_missile.pos_x, other_missile.pos_y)
        
        #-- 2. Delete the missiles from the DB -- #
        self.delete(other_missile)


    def act_accordingly_ship(self, missile,ship):
        from app.navy.services.ship_service import ship_service
        ship_service.update_hp(ship,missile.damage)

    #endregion
    
    #region: Logic associated with the movement of the missile (no collision logic)
    def mov_is_valid(self, missile, x, y):
        if utils.is_out_of_bounds(x, y) or navy_game_service.get_from_map(missile.navy_game_id, x, y):
            return False
        return True

    def move(self, missile):
        old_x,old_y = missile.pos_x,missile.pos_y
        #region: 1. Move the missile
        for _ in range(missile.speed):
            x,y = utils.get_next_position(missile.pos_x,missile.pos_y, missile.course)
            if not self.mov_is_valid(missile, x, y):
                self.act_accordingly(missile,x,y)
                return False
            missile.pos_x , missile.pos_y = x, y
        #endregion
        #region: 2. Update the missile in the DB ( if it has moved correctly)
        else:
            navy_game_service.delete_in_map(missile.navy_game_id, old_x, old_y)
            navy_game_service.add_to_map(missile.navy_game_id, missile.pos_x, missile.pos_y)
            missile_dao.add_or_update(missile)
        #endregion
        return True
    #endregion



   

missile_service = MissileService()
