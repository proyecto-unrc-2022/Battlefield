from turtle import position


class NavyUtils:
    # ---------- CLASS CONSTANTS --------- #
    COMPASS = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
        "NE": (-1, 1),
        "NW": (-1, -1),
        "SE": (1, 1),
        "SW": (1, -1),
    }
    X, Y = 0, 1
    ZERO, ONE = 0, 1
    ROWS, COLS = 10, 20
    TRUE, FALSE = 1, 0
    INVERSE_COORDS = {
        "N": "S",
        "S": "N",
        "W": "E",
        "E": "W",
        "SE": "NW",
        "NW": "SE",
        "SW": "NE",
        "NE": "SW",
    }
    DIRECTIONS = ["N", "S", "E", "W", "SE", "SW", "NE", "NW"]
    # ---------- END CLASS CONSTANTS --------- #

    # ---------- CLASS METHODS --------- #
    def get_next_position(self, x, y, course):
        if course in self.COMPASS:
            return (x + self.COMPASS[course][self.X], y + self.COMPASS[course][self.Y])

        return None

    def out_of_bounds(self, x, y):
        return x < self.ONE or x > self.ROWS or y < self.ONE or y > self.COLS

    def free_valid_poisition(self, x, y, navy_game_id):
        from app.navy.services.navy_game_service import navy_game_service

        return not self.out_of_bounds(x, y) and not navy_game_service.get_from_board(
            navy_game_id, x, y
        )

    def next_free_position(self, x, y, course, navy_game_id):
        from app.navy.services.navy_game_service import navy_game_service

        next_x, next_y = self.get_next_position(x, y, course)
        if self.free_valid_poisition(next_x, next_y, navy_game_id):
            return next_x, next_y
        return None


    # ---------- END OF CLASS METHODS --------- #


utils = NavyUtils()
