import functools

from app.navy.daos.navy_game_dao import navy_game_dao
from app.navy.models.navy_game import NavyGame
from app.navy.validators.navy_game_request_validator import NavyGameRequestValidator


class NavyGameService:

    games = {
        # id_game : {
        #    (x,y) : Missile
        #    (x_1,y_1): Ship
        # }
    }

    def add(self, request):
        navy_game_request_validator = NavyGameRequestValidator()
        validated_navy_game = navy_game_request_validator.load(request)
        navy_game = NavyGame(10, 20, validated_navy_game["user1_id"])
        navy_game_dao.add_or_update(navy_game)
        return navy_game

    def update_game(self, navy_game_id):
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
        actions = action_service.get(
            navy_game_id
        )  # TODO: refactor, (In this point actions could come from the parameters)

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
        return NavyGameDTO().dump(navy_game_dao.get(navy_game_id))

    def load_game_to_map(self, navy_game_id):
        from app.navy.services.missile_service import missile_service
        from app.navy.utils.navy_utils import NavyUtils

        # --------------- 1.Get missiles and ships from DB ---------------#
        missiles = missile_service.get(navy_game_id)
        ships = ship_service.get(navy_game_id)

        # --------------- 2. Load missiles and ships to map ---------------#
        """  
       self.state_game[navy_game_id] = {
            (missile.x,missile.y):missile for missile in missiles
            (x,y): ship for NavyUtils.re_build(ship) in ships
        } """

        # --------------- 3. Returned them ---------------#
        return missiles, ships

    def exist_any(self, navy_game_id):
        entity = self.games[navy_game_id]
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
