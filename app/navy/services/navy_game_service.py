from app.navy.daos.navy_game_dao import navy_game_dao
from app.navy.models.missile import Missile
from app.navy.models.navy_game import NavyGame
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

    def validate_post_request(self, request):
        return NavyGamePostValidator().load(request)

    def validate_patch_request(self, request):
        return NavyGamePatchValidator().load(request)

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

    def delete_from_board(self, navy_game_id, x, y):
        del self.games[navy_game_id][(x, y)]

    def load_to_board(self, navy_game_id, x, y, entity):
        self.games[navy_game_id][(x, y)] = entity

    def get_from_board(self, navy_game_id, x, y):
        return self.games[navy_game_id].get((x, y))

    def load_game(self, navy_game_id):
        from app.navy.services.missile_service import missile_service
        from app.navy.services.ship_service import ship_service

        ships = ship_service.get_by(navy_game_id=navy_game_id)
        missiles = missile_service.get(navy_game_id=navy_game_id)
        self.games[navy_game_id] = {
            "ships": ships,
            "missiles": missiles,
        }
        self.load_missiles_to_board(navy_game_id)
        self.load_ships_to_board(navy_game_id)

    def load_ships_to_board(self, navy_game_id):
        from app.navy.services.ship_service import ship_service

        ships = self.games[navy_game_id]["ships"]
        for ship in ships:
            ship_service.load_to_board(ship)

    def load_missiles_to_board(self, navy_game_id):
        from app.navy.services.missile_service import missile_service

        missiles = self.games[navy_game_id]["missiles"]
        for missile in missiles:
            missile_service.load_to_board(missile)

    def update_game(self, navy_game_id):
        from app.navy.services.action_service import action_service
        from app.navy.services.missile_service import missile_service

        if not self.games.get(navy_game_id):
            self.load_game(navy_game_id)

        # game = self.games[navy_game_id]
        game_db = navy_game_dao.get_by_id(navy_game_id)
        # missiles = missile_service.get(navy_game_id=game_db.id)
        missiles = self.games[navy_game_id]["missiles"]
        actions = action_service.get_by_round(navy_game_id, game_db.round)

        if self.update_missiles(missiles):
            actions.sort(key=lambda x: x.user_id == game_db.turn, reverse=True)
            for action in actions:
                if not action_service.execute(action) and self.check_winner(
                    navy_game_id
                ):
                    return
        game = self.change_turn(game=game_db)
        game.round += 1
        navy_game_dao.add_or_update(game)

    def update_missiles(self, missiles):
        from app.navy.services.missile_service import missile_service

        for missile in missiles:
            if not missile_service.update_position(missile) and self.check_winner(
                missile.navy_game_id
            ):
                return False
        return True

    def change_turn(self, navy_game_id=None, game=None):
        if not game:
            game = self.get_by_id(navy_game_id)

        game.turn = game.user1_id if game.turn == game.user2_id else game.user2_id
        return game

    def set_winner(self, winner, navy_game_id=None, game=None):
        if not game:
            game = self.get_by_id(navy_game_id)

        game.winner = winner
        navy_game_dao.add_or_update(game)

    def check_winner(self, navy_game_id):
        from app.navy.services.ship_service import ship_service

        game = self.get_by_id(navy_game_id)

        ships_user1 = ship_service.get_by(
            user_id=game.user1_id, navy_game_id=navy_game_id
        )
        ships_user2 = ship_service.get_by(
            user_id=game.user2_id, navy_game_id=navy_game_id
        )

        if not ships_user1:
            self.set_winner(game.user2_id, game=game)
            return True
        elif not ships_user2:
            self.set_winner(game.user1_id, game=game)
            return True
        return False

    def should_update(self, navy_game_id):
        from app.navy.services.action_service import action_service

        game = navy_game_dao.get_by_id(navy_game_id)
        actions = action_service.get_by_round(
            navy_game_id=navy_game_id, round=game.round
        )
        return len(actions) == 2

    def delete_entity(self, entity):
        from app.navy.models.missile import Missile
        from app.navy.models.ship import Ship

        if isinstance(entity, Ship):
            self.games[entity.navy_game_id]["ships"].remove(entity)
        elif isinstance(entity, Missile):
            self.games[entity.navy_game_id]["missiles"].remove(entity)

    def get_ship_from_game(self, navy_game_id, ship_id):
        ships = self.games[navy_game_id]["ships"]
        for ship in ships:
            if ship.id == ship_id:
                return ship
        return None


navy_game_service = NavyGameService()
