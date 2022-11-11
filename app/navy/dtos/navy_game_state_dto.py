class NavyGameStateDTO:
    def __init__(self, id, user_id) -> None:
        self.id = id
        self.user_id = user_id
        self.load_state()

    def load_ship(self, user_id):
        from app.navy.dtos.ship_dto import ShipDTO
        from app.navy.services.ship_service import ship_service
        from app.navy.utils.navy_utils import utils

        ships = ship_service.get_by(user_id=user_id)
        if ships:
            user_ship = ships[utils.ZERO]
            return ShipDTO().dump(user_ship)

    def load_state(self):
        from app.navy.services.navy_game_service import navy_game_service

        navy_game = navy_game_service.get_by_id(self.id)

        self.host = navy_game.user1_id
        self.guest = navy_game.user2_id
        self.rows = navy_game.board_rows
        self.cols = navy_game.board_colums
        self.ready_to_play = navy_game.ready_to_play
        self.turn = navy_game.turn
        self.round = navy_game.round
        self.winner = navy_game.winner
        self.ship = self.load_ship(self.user_id)
        self.sight_range = navy_game_service.get_board(self.id, self.user_id)

    def dump(self):
        return {
            "id": self.id,
            "host": self.host,
            "guest": self.guest,
            "rows": self.rows,
            "cols": self.cols,
            "ready_to_play": self.ready_to_play,
            "turn": self.turn,
            "round": self.round,
            "winner": self.winner,
            "ship": self.ship,
            "sight_range": self.sight_range,
        }
