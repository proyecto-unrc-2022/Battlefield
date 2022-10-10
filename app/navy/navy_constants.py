# File for constants used in the navy app
PATH_TO_START = "app/navy/start.json"
PATH_TO_SHIP_TYPES = "app/navy/ship_types.json"
ROWS = 10
COLS = 20
DIRECTIONS = ["N", "S", "E", "W", "SE", "SW", "NE", "NW"]
MISSILES_TYPES = [1, 2, 3, 4]
TRUE = 1
FALSE = 0
MINIMUM_HP = 0
FIRST = 0
SECOND = 1
ZERO = 0
ONE = 1
EMPTY_LIST = []
SHIP_TYPES = [1, 2, 3, 4]

BORDERS = {
    "top": 1,
    "bottom": ROWS,
    "left": 1,
    "right": COLS,
}
XCORD = 0
YCORD = 1
COORDS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (1, -1),
}
