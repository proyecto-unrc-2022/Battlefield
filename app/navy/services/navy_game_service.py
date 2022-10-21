from app.navy.daos.navy_game_dao import navy_game_dao
from app.navy.models.navy_game import NavyGame
from app.navy.services.ship_service import ship_service
from app.navy.utils.navy_utils import utils
from app.navy.validators.navy_game_patch_validator import NavyGamePatchValidator
from app.navy.validators.navy_game_post_validator import NavyGamePostValidator

""" Navy Game Service
    This class is responsible for all the business logic related to the Navy Game
    Attributes:
        games (list): List of all the games in the system.
    Methods:
        This class provides the following methods:
        validate_post_request(self, request)
        validate_patch_request(self, request)
        add(self,data)
        join_second_player(self,data,id)
        get_all(self,user_id=None)
        get_by_id(self,id)
        delete(self,id)
        delete_in_map
        add_in_map
        get_from_map
        update_game
        change_turn
        set_winner
        end_game

    You can view in github the source code of this class:
    navy_game_service: https://github.com/proyecto-unrc-2022/Battlefield/tree/develop/app/navy
"""


class NavyGameService:

    games = {}

    # region Validation's Logic
    def validate_post_request(self, request):
        return NavyGamePostValidator().load(request)

    def validate_patch_request(self, request):
        return NavyGamePatchValidator().load(request)

    # endregion

    # region Game's Logic Methods for BD
    def add(self, data):
        new_game = NavyGame(utils.ROWS, utils.COLS, data["user1_id"])
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

    # endregion

    # region Game's Logic Methods for memory map "self.games"
    def load_game_to_map(self, navy_game_id):
        from app.navy.services.missile_service import missile_service

        # --------------- 1.Get missiles and ships from DB ---------------#
        self.games[navy_game_id] = {}
        missiles = missile_service.get(navy_game_id=navy_game_id)
        ships = ship_service.get_by(navy_game_id=navy_game_id)

        # --------------- 2. Load missiles and ships to map ---------------#
        for ship in ships:
            ship_service.add_to_map(ship)

        if missiles:
            for missile in missiles:
                missile_service.add_in_map(missile)
            return missiles
        return []
        # --------------- 3. Returned them ---------------#

    def delete_from_map(self, navy_game_id, x, y):
        del self.games[navy_game_id][(x, y)]

    def add_in_map(self, navy_game_id, x, y, entity):
        self.games[navy_game_id][(x, y)] = entity

    def get_from_map(self, navy_game_id, x, y):
        return self.games[navy_game_id].get((x, y))

    # endregion

    def update_game(self, navy_game_id):
        # region:  --------------- 1. Neccesary Imports ---------------#
        from app.navy.services.action_service import action_service
        from app.navy.services.missile_service import missile_service

        # endregion
        # region: --------------- 2. Get game,missiles and actions ---------------#
        actions = action_service.get_by_navy_game(navy_game_id)
        missiles = self.load_game_to_map(navy_game_id)
        game = self.get_by_id(navy_game_id)
        # endregion
        # region: --------------- 3. Update the game - Move the missiles ---------------#

        for missile in missiles:
            # move
            # check if hit
            #   act!
            if not missile_service.move(missile):
                game = self.end_game(navy_game_id)
                if game.winner:
                    return
        # endregion
        # region: --------------- 4. Update the game - Execute Actions associated ---------------#
        actions.sort(key=lambda x: x.user_id == game.turn, reverse=True)

        for action in actions:
            if not action_service.execute(action):
                game = self.end_game(navy_game_id)
                if game.winner:
                    return
        else:
            action_service.delete_all(navy_game_id)
        # endregion
        # region: --------------- 5. Update region:   the game - Change turn ---------------#
        game = self.change_turn(game=game)
        game.round += 1
        navy_game_dao.add_or_update(game)
        # endregion

    def change_turn(self, navy_game_id=None, game=None):
        # region: --------------- 1. Logic parameter's ---------------#
        if not game:
            game = self.get_by_id(navy_game_id)
        # endregion

        game.turn = game.user1_id if game.turn == game.user2_id else game.user2_id
        return game

    def set_winner(self, winner, navy_game_id=None, game=None):
        # region: --------------- 1. Logic parameter's ---------------#
        if not game:
            game = self.get_by_id(navy_game_id)
        # endregion

        game.winner = winner
        navy_game_dao.add_or_update(game)
        return game

    def end_game(self, navy_game_id):
        # region --------------- 1. Get Game and ship (from BD) ---------------#
        ships = ship_service.get_by(navy_game_id=navy_game_id)
        game = self.get_by_id(navy_game_id)
        # endregion

        ships_user1 = ship_service.get_by(
            user_id=game.user1_id, navy_game_id=navy_game_id
        )
        ships_user2 = ship_service.get_by(
            user_id=game.user2_id, navy_game_id=navy_game_id
        )

        # region --------------- 3. Check if are a Winner ---------------#
        if not ships_user1:
            self.set_winner(game.user2_id, game=game)
        elif not ships_user2:
            self.set_winner(game.user1_id, game=game)
        # endregion
        return game

    def should_update(self, navy_game_id):
        from app.navy.services.action_service import action_service

        actions = action_service.get_by_navy_game(navy_game_id=navy_game_id)
        return (
            len(actions) == 2
        )  # refactor this, len(actions) == len(users in game) TODO: len(users)


navy_game_service = NavyGameService()
