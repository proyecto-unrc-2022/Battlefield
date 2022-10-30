from app import db
from app.underwater.models.submarine import Submarine
from app.underwater.models.torpedo import Torpedo


class BoardProxy(db.Model):
    def __init__(self, game):
        self.board = game.board
        self.proxy_dict = {}
        self.radar_scope = []

    def update_cell(self, player, i, j):
        matrix = self.board.matrix
        if (i, j) in player.submarine.vision_scope():
            if matrix[i][j]:
                d = {j: self.encode(matrix[i][j], player, i, j)}
                self.proxy_dict.update({i: d})
        elif (i, j) in player.submarine.radar_scope():
            if matrix[i][j]:
                d = {j: "rP"}
            else:
                d = {j: "rN"}
            self.proxy_dict.update({i: d})

    def get_radar_pulse(self):
        self.radar_scope.clear()

    def get_board(self, player):
        matrix = self.board.matrix
        visible_board = {}
        for i in range(self.board.height):
            for j in range(self.board.width):
                if (i, j) in player.submarine.vision_scope():
                    if matrix[i][j]:
                        d = {j: self.encode(matrix[i][j], player, i, j)}
                        visible_board.update({i: d})
                elif (i, j) in player.submarine.radar_scope():
                    if matrix[i][j]:
                        d = {j: "rP"}
                    else:
                        d = {j: "rN"}
                    visible_board.update({i: d})

    def encode(self, obj, player, i, j):
        str = ""

        if obj.player is player:
            str += "F"
        else:
            str += "E"

        if isinstance(obj, Submarine):
            if (i, j) == obj.get_head_position():
                str += "H"
            else:
                str += "Ta"

        elif isinstance(obj, Torpedo):
            str += "To"
        str += str(obj.direction)
        return str

        # {(1: {2: "1H"},
        #   (3: {3: "rP"},
        #    (3: {2: "rN"})}
