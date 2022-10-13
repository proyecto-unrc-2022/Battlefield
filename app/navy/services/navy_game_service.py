from app.navy.daos.navy_game_dao import navy_game_dao
from app.navy.models.navy_game import NavyGame
from app.navy.validators.navy_game_request_validator import NavyGameRequestValidator


class NavyGameService:

    state_game = {}

    def add(self, request):
        navy_game_request_validator = NavyGameRequestValidator()
        validated_navy_game = navy_game_request_validator.load(request)
        navy_game = NavyGame(10, 20, validated_navy_game["user1_id"])
        navy_game_dao.add_or_update(navy_game)
        return navy_game

    def update_game(self, navy_game_id, actions):
        from app.navy.services.missile_service import missile_service

        game = navy_game_dao.get_by_id(navy_game_id)
        missiles = missile_service.get(navy_game_id)
        self.state_game[navy_game_id] = {
            (missile.x, missile.y): missile for missile in missiles
        }

        game.set_state_game({"missiles": missiles})

        for missile in missiles:
            missile_service.move(missile)
            pass

    def exist_missile(self, navy_game_id, x, y):
        if (x, y) in self.state_game[navy_game_id]:
            return self.state_game[navy_game_id][(x, y)]
        return None


navy_game_service = NavyGameService()
