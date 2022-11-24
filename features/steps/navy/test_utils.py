class TestUtils:

    EXPECTED_ERRORS = {
        "Game not found": "_schema",
        "Ship can't be builded in this position": "_schema",
        "Invalid action": "_schema",
        "Must be one of: N, S, E, W, SE, SW, NE, NW.": "course",
        "Can't move more than 3 spaces": "_schema",
        "The move is a negative distance": "_schema",
        "Invalid ship in game": "_schema",
        "Game not started yet": "_schema",
        "Game finished": "_schema",
        "It's not your turn yet": "_schema",
        "Ship can't be builded out of range": "_schema",
        "Must be one of: Destroyer, Cruiser, Battleship, Corvette.": "name",
        "Ship can't be builded out of range": "_schema",
    }

    def add_test_game(self, navy_game_id, winner=None, status="STARTED"):
        from app.navy.daos.navy_game_dao import navy_game_dao

        navy_game = navy_game_dao.get_by_id(navy_game_id)
        navy_game.status = status
        navy_game.winner = winner
        navy_game_dao.add(navy_game)

        return navy_game

    def json_action(
        self,
        user_id,
        course,
        attack,
        navy_game_id,
        missile_type_id,
        ship_id,
        move,
        round=None,
    ):
        return {
            "user_id": user_id,
            "course": course,
            "attack": attack,
            "navy_game_id": navy_game_id,
            "missile_type_id": missile_type_id,
            "ship_id": ship_id,
            "move": move,
            "round": round or 1,
        }

    def json_ship(self, name, pos_x, pos_y, course, user_id, navy_game_id):
        return {
            "name": name,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "course": course,
            "user_id": user_id,
            "navy_game_id": navy_game_id,
        }

    def add_test_ship(
        self,
        name,
        pos_x,
        pos_y,
        course,
        user_id,
        navy_game_id,
        hp=None,
        size=None,
        speed=None,
        visibility=None,
        missile_type_id=None,
    ):
        from app.navy.daos.ship_dao import ship_dao
        from app.navy.daos.ship_type_dao import ship_type_dao
        from app.navy.models.ship import Ship

        ship_data = ship_type_dao.get_by(name)
        new_ship = Ship(
            name,
            hp or ship_data["hp"],
            size or ship_data["size"],
            speed or ship_data["speed"],
            visibility or ship_data["visibility"],
            missile_type_id or ship_data["missile_type_id"][0],
            pos_x,
            pos_y,
            course,
            user_id,
            navy_game_id,
        )

        return ship_dao.add(new_ship)

    def add_test_missile(
        self,
        course,
        pos_x,
        pos_y,
        ship_id,
        navy_game_id,
        missile_type,
        damage=None,
        speed=None,
    ):

        from app.navy.daos.missile_dao import missile_dao
        from app.navy.daos.missile_type_dao import missile_type_dao
        from app.navy.models.missile import Missile

        missile_data = missile_type_dao.get_by_id(str(missile_type))
        missile = Missile(
            speed or missile_data["speed"],
            damage or missile_data["damage"],
            course,
            pos_x,
            pos_y,
            ship_id,
            navy_game_id,
        )

        return missile_dao.add(missile)

    def add_action_test(
        self,
        navy_game_id,
        ship_id,
        course,
        move,
        attack,
        missile_type_id,
        user_id,
        round,
    ):
        from app.navy.daos.action_dao import action_dao
        from app.navy.models.action import Action

        action = Action(
            navy_game_id, ship_id, course, move, attack, missile_type_id, user_id, round
        )
        action_dao.add_or_update(action)
        return action

    def generate_username_and_email(self, id):
        username = "user" + str(id)
        email = "user" + str(id) + "@user" + str(id) + ".com"
        return username, email

    def get_header(self, token):
        return {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token["token"]}',
        }


test_utils = TestUtils()
