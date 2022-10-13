from app.navy.daos.missile_dao import missile_dao
from app.navy.models.missile import Missile
from app.navy.models.ship import Ship
from app.navy.services.navy_game_service import navy_game_service
from app.navy.utils.navy_utils import utils


class MissileService:
    MISSILE_TYPES = [1, 2, 3, 4]

    def get(self, navy_game_id):
        missiles = missile_dao.get_by_navy_game_id(navy_game_id)
        return missiles.sort(key=lambda x: x.order)

    def action_on_contact(self, missile, entity):
        """ match entity:
            case Ship():
                self.action_on_contact_ship(missile, entity)
            case Missile():
                self.action_on_contact_missile(missile, entity)
 """
    def action_on_contact_ship(self, missile, ship):
        # TODO:
        return missile

    def action_on_contact_missile(self, missile, missile_contact):
        missile_dao.delete(missile)
        missile_dao.delete(missile_contact)

    def a(a: int):
        a + "a"
        pass

    def move(self, missile):
        for _ in range(missile.speed):
            x, y = utils.get_next_position(missile.x, missile.y, missile.course)
            entity = navy_game_service.exist_any(missile.navy_game_id, x, y)
            if entity:
                self.action_on_contact(missile, entity)
                break
            else:
                missile.set_position(x, y)

        missile_dao.add_or_update(missile)


missile_service = MissileService()
