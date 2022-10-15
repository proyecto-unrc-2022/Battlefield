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


test_utils = TestUtils()
