from app.navy.daos.navy_game_dao import navy_game_dao
from app.navy.models.missile import Missile
from app.navy.models.navy_game import NavyGame
from app.navy.utils.navy_game_statuses import FINISHED
from app.navy.utils.navy_utils import utils


class NavyGameService:

    games = {}

    def add(self, data):
        new_game = NavyGame(utils.ROWS, utils.COLS, data["user1_id"])
        navy_game_dao.add(new_game)
        self.games[new_game.id] = {}
        return new_game

    def join(self, data):
        game = navy_game_dao.get_by_id(data["game_id"])
        game.user2_id = data["user2_id"]
        navy_game_dao.update(game, commit=True)
        return game

    def get_all(self, user_id=None):
        if user_id:
            return navy_game_dao.get_by_user(user_id)
        else:
            return navy_game_dao.get_all()

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
        entity = self.games[navy_game_id].get((x, y))
        if entity and entity.is_alive:
            return entity
        return None

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

    def get_ships(self, navy_game_id):
        return self.games[navy_game_id]["ships"]

    def execute_cache(f):
        def proceed(self, navy_game_id):
            if not self.games.get(navy_game_id):
                self.load_game(navy_game_id)
                return f(self, navy_game_id)
            else:
                return f(self, navy_game_id)

        return proceed

    @execute_cache
    def play_round(self, navy_game_id):
        game = navy_game_dao.get_by_id(navy_game_id)
        self.run_missiles(game)
        self.run_actions(game)
        self.finalize_round(game)
        self.save(game)

    def finalize_round(self, game):
        self.is_over(game.id)
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
        from app.navy.services.spectate_service import spectate_service

        ships = self.games[game.id]["ships"]
        missiles = self.games[game.id]["missiles"]

        ship_service.update_all(ships)
        missile_service.update_all(missiles)
        navy_game_dao.update(game)
        spectate_service.save_round(game, ships, missiles)

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
        game.status = FINISHED

    def is_over(self, navy_game_id):
        game = navy_game_dao.get_by_id(navy_game_id)
        is_game_over = True
        if game.winner:
            return is_game_over
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

    def get_visibility(self, navy_game_id, user_id):
        from app.navy.services.ship_service import ship_service

        game_board = self.get_board(navy_game_id)
        user_ships = ship_service.get_by(user_id=user_id, navy_game_id=navy_game_id)
        entities = set([])

        for ship in user_ships:
            for pos in game_board:
                if ship_service.pos_in_range(ship, pos):
                    entities.add(game_board[pos])

        ships_dto, missiles_dto = self.to_dto(entities, user_id)
        return {"ships": ships_dto, "missiles": missiles_dto}

    @execute_cache
    def get_board(self, navy_game_id):
        game_dict = self.games[navy_game_id].copy()
        game_dict.pop("ships")
        game_dict.pop("missiles")
        return game_dict

    def to_dto(self, entities, user_id):
        from app.navy.models.ship import Ship
        from app.navy.services.missile_service import missile_service
        from app.navy.services.ship_service import ship_service

        ships_dto = []
        missiles_dto = []

        for entity in entities:
            if isinstance(entity, Ship) and entity.user_id != user_id:
                ships_dto.append(ship_service.get_dto(entity))
            elif isinstance(entity, Missile):
                missiles_dto.append(missile_service.get_dto(entity))
        return ships_dto, missiles_dto


navy_game_service = NavyGameService()
