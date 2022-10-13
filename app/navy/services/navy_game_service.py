import functools

from app.navy.daos.navy_game_dao import navy_game_dao
from app.navy.models.navy_game import NavyGame
from app.navy.validators.navy_game_post_validator import NavyGamePostValidator
from app.navy.validators.navy_game_patch_validator import NavyGamePatchValidator
from app.navy.services.ship_service import ship_service


class NavyGameService:

    games = {
        # id_game : {
        #    (x,y) : Missile
        #    (x_1,y_1): Ship
        # }
    }

    def validate_post_request(self, request):
        validated_data = NavyGamePostValidator().load(request)
        return validated_data

    def validate_patch_request(self, request):
        validated_data = NavyGamePatchValidator().load(request)
        return validated_data

    def add(self, data):
        new_game = NavyGame(10, 20, data["user1_id"])
        navy_game_dao.add_or_update(new_game)
        return new_game

    def join_second_player(self, data, id):
        game = navy_game_dao.get_by_id(id)
        game.user2_id = data["user2_id"]
        navy_game_dao.add_or_update(game)
        return game 

    def get_all(self, user_id=None):
        if user_id:
            return navy_game_dao.get_by_user(user_id)
        else:
            return navy_game_dao.get()

    def get_by_id(self, id):
        return navy_game_dao.get_by_id(id) 

    def delete(self, id):
        game = navy_game_dao.get_by_id(id)
        navy_game_dao.delete(game)
        return game

    def update_game(self, navy_game_id, actions):
        # --------------- 1. IMPORTS SECTIONS ---------------#
        from app.navy.dtos.navy_game_dto import NavyGameDTO
        from app.navy.models.action import Action
        from app.navy.services.missile_service import missile_service

        # --------------- 2. Get missiles and ships ---------------#
        missiles, ships = self.load_game_to_map(navy_game_id)

        # --------------- 3. Update the game - Move the missiles ---------------#
        map(
            missile_service.move, missiles
        )  # Note: missiles already sorted by 'order' field

        for (
            action
        ) in (
            actions
        ):  # otra opción es que action_service tenga un execute , action_service.execute(action)
            # if action.type == "MOVE" ...
            user_ships = filter(lambda ship: ship.user_id == action.user_id, ships)
            map(
                lambda ship: ship_service.move(ship)
                if not action.attack
                else ship_service.attack(ship),
                user_ships,
            )

        # --------------- 4. Return the game ---------------#
        # return NavyGameDTO().dump(navy_game_dao.get(navy_game_id))

    def load_game_to_map(self, navy_game_id):
        from app.navy.services.missile_service import missile_service
        from app.navy.utils.navy_utils import NavyUtils

        # --------------- 1.Get missiles and ships from DB ---------------#
        missiles = missile_service.get(navy_game_id)
        ships = ship_service.get(navy_game_id)

        # --------------- 2. Load missiles and ships to map ---------------#
        return missiles, ships

    """  
      self.state_game[navy_game_id] = {
            (missile.x,missile.y):missile for missile in missiles
            (x,y): ship for NavyUtils.re_build(ship) in ships
        } 
        """
    # --------------- 3. Returned them ---------------#

    def exist_any(self, navy_game_id, x, y):
        entity = self.games[navy_game_id][(x, y)]
        return entity is not None

    """ 
        def get_missiles(self,navy_game_id):
        res = []
        for key in self.games[navy_game_id].keys():
            if isinstance(self.games[navy_game_id][key],Missile):
                res.append(self.games[navy_game_id][key])
        return res
     """


navy_game_service = NavyGameService()
