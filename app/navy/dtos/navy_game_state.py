class NavyGameState:
    def __init__(self, id, user_id) -> None:
        self.id = id
        self.user_id = user_id
        self.rows = None
        self.cols = None
        self.ready_to_play = None
        self.turn = None
        self.round = None
        self.winner = None
        self.ship = None
        self.board = None
        self.load_state()

    def load_ship(self, user_id):
        from app.navy.dtos.ship_dto import ShipDTO
        from app.navy.services.ship_service import ship_service

        user_ship = ship_service.get_by(user_id=user_id)[0]
        return ShipDTO().dump(user_ship)

    def load_state(self):
        from app.navy.services.navy_game_service import navy_game_service
        from app.navy.services.ship_service import ship_service

        navy_game = navy_game_service.get_by_id(self.id)
        self.rows = navy_game.board_rows
        self.cols = navy_game.board_colums
        self.ready_to_play = navy_game.ready_to_play
        self.turn = navy_game.turn
        self.round = navy_game.round
        self.winner = navy_game.winner
        self.ship = self.load_ship(self.user_id)
        self.board = navy_game_service.get_board(self.id, self.user_id)

    def dump(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "rows": self.rows,
            "cols": self.cols,
            "ready_to_play": self.ready_to_play,
            "turn": self.turn,
            "round": self.round,
            "winner": self.winner,
            "ship": self.ship,
            "board": self.board,
        }
