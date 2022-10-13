TRUE = 1
FALSE = 0


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

    # ---------- CLASS METHODS --------- #
    def get_next_position(self, x, y, course):
        if course in self.COMPASS:
            return (x + self.COMPASS[course][self.X], y + self.COMPASS[course][self.Y])

        return None

    # ---------- END OF CLASS METHODS --------- #


navy_utils = NavyUtils()
