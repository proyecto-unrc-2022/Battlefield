class SpectateService:

    games_spec = {}

    def save_round(self, game, ships, missiles):
        if game.id not in self.games_spec:
            self.games_spec[game.id] = {}
        ships, missiles = self.process_entities(ships, missiles)

        if game.round not in self.games_spec[game.id]:
            self.games_spec[game.id].update(
                {
                    **self.games_spec[game.id],
                    game.round: {"ships": ships, "missiles": missiles},
                }
            )

    def get_ships(self, game_id, round):
        return self.games_spec[game_id][round]["ships"]

    def get_missiles(self, game_id, round):
        return self.games_spec[game_id][round]["missiles"]

    def process_ship(self, ship):
        from app.navy.services.ship_service import ship_service

        ship_temp = ship_service.create(
            ship.name,
            ship.pos_x,
            ship.pos_y,
            ship.course,
            ship.user_id,
            ship.navy_game_id,
        )
        ship_temp.id = ship.id
        ship_temp.is_alive = ship.is_alive
        ship_temp.hp = ship.hp
        return ship_temp

    def process_missile(self, missile):
        from app.navy.services.missile_service import missile_service
        from app.navy.services.ship_service import ship_service

        missile_type_id = ship_service.get_by_id(missile.ship_id).missile_type_id
        missile_temp = missile_service.create(
            navy_game_id=missile.navy_game_id,
            ship_id=missile.ship_id,
            missile_type=missile_type_id,
            pos_x=missile.pos_x,
            pos_y=missile.pos_y,
            course=missile.course,
        )
        missile_temp.id = missile.id
        missile_temp.is_alive = missile.is_alive
        return missile_temp

    def process_entities(self, ships, missiles):
        ships_copy = []
        missiles_copy = []
        for ship in ships:
            ships_copy.append(self.process_ship(ship))
        for missile in missiles:
            missiles_copy.append(self.process_missile(missile))
        return ships_copy, missiles_copy


spectate_service = SpectateService()
