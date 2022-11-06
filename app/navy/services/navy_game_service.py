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
        self.games[new_game.id] = {}
        return new_game

    def join(self, data, id):
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
        ships = [ship for ship in ships if ship.is_alive]
        missiles = [missile for missile in missiles if missile.is_alive]
        self.games[navy_game_id] = {
            "ships": ships,
            "missiles": missiles,
        }
        self.load_missiles(navy_game_id)
        self.load_ships(navy_game_id)

    def load_ships(self, navy_game_id):
        from app.navy.services.ship_service import ship_service

        ships = self.games[navy_game_id]["ships"]
        for ship in ships:
            ship_service.load_to_board(ship)

    def load_missiles(self, navy_game_id):
        from app.navy.services.missile_service import missile_service

        missiles = self.games[navy_game_id]["missiles"]
        for missile in missiles:
            missile_service.load_to_board(missile)

    def get_missiles(self, navy_game_id):
        return self.games[navy_game_id]["missiles"]

    def execute_cache(f):
        def proceed(self, navy_game_id):
            if not self.games.get(navy_game_id):
                self.load_game(navy_game_id)
                f(navy_game_id)
            else:
                f(navy_game_id)

        return proceed

    @execute_cache
    def play_round(self, navy_game_id):
        game = navy_game_dao.get_by_id(navy_game_id)
        self.run_missiles(game)
        self.run_actions(game)
        self.finalize_round(game)
        self.save(game)

    def finalize_round(self, game):
        game.round += 1
        game.turn = self.change_turn(game)

    def run_actions(self, game):
        from app.navy.services.action_service import action_service

        actions = action_service.get_by_round(game.id, game.round, game.turn)
        for action in actions:
            if action_service.can_execute(action):
                action_service.execute(action)

    def save(self, game):
        from app.navy.services.missile_service import missile_service
        from app.navy.services.ship_service import ship_service

        ships = self.games[game.id]["ships"]
        missiles = self.games[game.id]["missiles"]
        for ship in ships:
            ship_service.update_db(ship)
        for missile in missiles:
            missile_service.update_db(missile)
        navy_game_dao.add_or_update(game)

    def run_missiles(self, game):
        from app.navy.services.missile_service import missile_service

        missiles = missile_service.get_alives(game.id)
        for missile in missiles:
            missile_service.update_position(missile)

    def change_turn(self, game):
        game.turn = game.user1_id if game.turn == game.user2_id else game.user2_id
        return game.turn

    def set_winner(self, winner, game):
        game.winner = winner
        navy_game_dao.add_or_update(game)

    def is_over(self, navy_game_id):
        game = navy_game_dao.get_by_id(navy_game_id)
        is_game_over = True
        if game.winner:
            pass
        elif self.user_lost(game.user1_id, navy_game_id):
            self.set_winner(game.user2_id, game=game)

        elif self.user_lost(game.user2_id, navy_game_id):
            self.set_winner(game.user1_id, game=game)

        else:
            is_game_over = False

        return is_game_over

    def user_lost(self, user_id, navy_game_id):
        from app.navy.services.ship_service import ship_service

        ships = ship_service.get_alives(user_id, navy_game_id)
        return not ships

    def should_update(self, navy_game_id):
        from app.navy.services.action_service import action_service

        game = navy_game_dao.get_by_id(navy_game_id)
        actions = action_service.get_by_round(
            navy_game_id=navy_game_id, round=game.round, turn=game.turn
        )
        return len(actions) == utils.CANT_PLAYERS

    def get_ship_from_game(self, navy_game_id, ship_id):
        ships = self.games[navy_game_id]["ships"]
        for ship in ships:
            if ship.id == ship_id:
                return ship
        return None

    def get_active_games(self):
        keys_games = self.games.keys()
        games = []
        for key in keys_games:
            game = self.get_by_id(key)
            if not game.winner:
                games.append(game)
        return games

    def get_board(self, navy_game_id, user_id):
        from app.navy.services.missile_service import missile_service
        from app.navy.services.ship_service import ship_service

        if not self.games.get(navy_game_id):
            self.load_game(navy_game_id)

        # -------- NavyGameState reemplaza estas 3 lineas -----#
        game_dict = self.games[navy_game_id].copy()
        game_dict.pop("ships")
        game_dict.pop("missiles")
        # ------------------------------------------------------#

        user_ships = ship_service.get_by(user_id=user_id, navy_game_id=navy_game_id)
        set_ships = set([])
        set_missiles = set([])

        for ship in user_ships:
            sight_range = ship_service.get_sight_range(ship)
            for x, y in game_dict.keys():
                if utils.get_distance(ship.pos_x, ship.pos_y, x, y) <= sight_range:
                    visible_entity = self.get_from_board(ship.navy_game_id, x, y)
                    self.add_to_set(visible_entity, set_ships, set_missiles, ship.id)

        ships = list(map(ship_service.get_dto, set_ships))
        missiles = list(map(missile_service.get_dto, set_missiles))

        return {"ships": ships, "missiles": missiles}

    def add_to_set(self, entity, set_ships, set_missiles, ship_id):
        from app.navy.models.ship import Ship

        if isinstance(entity, Ship) and entity.id != ship_id:
            set_ships.add(entity)
        elif isinstance(entity, Missile):
            set_missiles.add(entity)

    def get_ships(self, navy_game_id):
        return self.games[navy_game_id]["ships"]


navy_game_service = NavyGameService()
