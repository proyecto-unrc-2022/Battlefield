from app.models.user import User, UserSchema


class NavyGameStateDTO:
    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id
        self.load_state()

    def load_ship(self, user_id, navy_game_id):
        from app.navy.dtos.ship_dto import ShipDTO
        from app.navy.services.ship_service import ship_service
        from app.navy.utils.navy_utils import utils

        ships = ship_service.get_by(user_id=user_id, navy_game_id=navy_game_id)
        if ships:
            user_ship = ships[utils.ZERO]
            return ShipDTO().dump(user_ship)

    def load_state(self):
        from app.navy.services.navy_game_service import navy_game_service

        navy_game = navy_game_service.get_by_id(self.id)
        user_1 = User.query.filter_by(id=navy_game.user1_id).first()
        user_2 = User.query.filter_by(id=navy_game.user2_id).first()

        self.user_1 = UserSchema().dump(user_1)
        self.user_2 = UserSchema().dump(user_2)
        self.rows = navy_game.rows
        self.cols = navy_game.cols
        self.status = navy_game.status
        self.turn = navy_game.turn
        self.round = navy_game.round
        self.winner = navy_game.winner
        self.ship = self.load_ship(self.user_id, self.id)
        self.sight_range = []
        if navy_game.status == "STARTED":
            self.sight_range = navy_game_service.get_visibility(self.id, self.user_id)

    def dump(self):
        return {
            "id": self.id,
            "user_1": self.user_1,
            "user_2": self.user_2,
            "rows": self.rows,
            "cols": self.cols,
            "status": self.status,
            "turn": self.turn,
            "round": self.round,
            "winner": self.winner,
            "ship": self.ship,
            "sight_range": self.sight_range,
        }
