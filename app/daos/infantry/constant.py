EAST = 2
SOUTH_EAST = 3
SOUTH = 4
SOUTH_WEST = 5
WEST = 6
NORTH_WEST = 7
NORTH = 0
NORTH_EAST = 1

COORDS_CUERPO = {
    0 : (0, -1), #N
    1 : (-1, -1), #NE
    2 : (-1, 0), #E
    3 : (-1, 1), #SE
    4 : (0, 1), #S
    5 : (1, 1), #SO
    6 : (1, 0), #O
    7 : (1, -1), #NO
}

COORDS_MISIL = {
    0 : (0, -1), #S
    1 : (-1, -1), #SO
    2 : (-1, 0), #0
    3 : (-1, 1), #NO
    4 : (0, 1), #N
    5 : (1, 1), #NE
    6 : (1, 0), #E
    7 : (1, -1), #SE
}

MACHINE_GUN = 0
MISSILE = 1
MORTAR = 2

SOLDIER = 1
HUMVEE = 2
TANK = 3
ARTILLERY = 4