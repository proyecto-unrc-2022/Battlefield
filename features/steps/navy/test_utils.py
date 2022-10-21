class TestUtils:
    def json_action(
        self, user_id, course, attack, navy_game_id, missile_type_id, ship_id, move
    ):
        return {
            "user_id": user_id,
            "course": course,
            "attack": attack,
            "navy_game_id": navy_game_id,
            "missile_type_id": missile_type_id,
            "ship_id": ship_id,
            "move": move,
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

        return ship_dao.add_or_update(new_ship)

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
        order=None,
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
            order or 1,
        )

        return missile_dao.add_or_update(missile)

    
    def add_action_test(self, navy_game_id, ship_id, course, move, attack, missile_type_id, user_id):
        from app.navy.models.action import Action
        from app.navy.daos.action_dao import action_dao

        action = Action(navy_game_id, ship_id, course, move, attack, missile_type_id, user_id)
        action_dao.add_or_update(action)
        return action

test_utils = TestUtils()
