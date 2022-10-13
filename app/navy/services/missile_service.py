from app.navy.daos.missile_dao import missile_dao
from app.navy.services.navy_game_service import navy_game_service
from app.navy.utils.navy_utils import navy_utils


class MissileService:
    MISSILE_TYPES = [1, 2, 3, 4]

    def get(self, navy_game_id):
        missiles = missile_dao.get_by_navy_game_id(navy_game_id)
        return missiles.sort(key=lambda x: x.order)

    def move(self, missile):
        x, y = navy_utils.get_next_position(missile.x, missile.y, missile.course)
        missile_intercepted = navy_game_service.exist_missile(
            missile.navy_game_id, x, y
        )

        if missile_intercepted:
            self.destroy_two(missile, missile_intercepted)

    def destroy_two(self, m1, m2):
        missile_dao.delete(m1)
        missile_dao.delete(m2)


missile_service = MissileService()
