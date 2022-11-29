from app.navy.services.spectate_service import spectate_service


class NavyGameSpectateDTO:
    def __init__(self, navy_game_id, round):
        self.navy_game_id = navy_game_id
        self.round = round
        self.load_game_info()

    def load_game_info(self):
        from app.navy.services.navy_game_service import navy_game_service
        from app.navy.services.ship_service import ship_service
        from app.navy.services.missile_service import missile_service

        self.game = navy_game_service.get_by_id(self.navy_game_id)
        if self.round == 0:
            self.round = self.game.round - 1
        ships = spectate_service.get_ships(self.navy_game_id, self.round)
        missiles = spectate_service.get_missiles(self.navy_game_id, self.round)
        self.ships = [ship_service.get_dto(ship) for ship in ships]
        self.missiles = [missile_service.get_dto(missile) for missile in missiles]

    def dump(self):
        from app.navy.dtos.navy_game_dto import NavyGameDTO

        return {
            "game": NavyGameDTO().dump(self.game),
            "ships": self.ships,
            "missiles": self.missiles,
        }
