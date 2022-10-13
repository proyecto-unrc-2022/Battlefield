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

    DIRECTIONS = ["N", "S", "E", "W", "SE", "SW", "NE", "NW"]
    # ---------- CLASS METHODS --------- #
    def get_next_position(self, x, y, course):
        if course in self.COMPASS:
            return (x + self.COMPASS[course][self.X], y + self.COMPASS[course][self.Y])

        return None

    # ---------- END OF CLASS METHODS --------- #


    def re_build(self, orientation, x, y, size):
        res = []
        if orientation in self.INVERSE_COORDS:
            for i in range(size):
                x, y = self.get_next_position(x, y, self.INVERSE_COORDS[orientation])
                res.append((x, y))
        return res

    # ---------- END OF CLASS METHODS --------- #


utils = NavyUtils()
