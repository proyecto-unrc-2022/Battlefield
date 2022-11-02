from app import db
from app.underwater.models.submarine import Submarine
from app.underwater.models.torpedo import Torpedo


class BoardMask(db.Model):
    def __init__(self, game, player):
        self.board = game.board
        self.player = player
        self.mask_dict = {}
        self.radar_cells = []
        self.visible_cells = []

    # def update_cell(self, player, i, j):
    #     matrix = self.board.matrix
    #     if (i, j) in player.submarine.vision_scope():
    #         if matrix[i][j]:
    #             d = {j: self.encode(matrix[i][j], player, i, j)}
    #             self.mask_dict.update({i: d})
    #     elif (i, j) in player.submarine.radar_scope():
    #         if matrix[i][j]:
    #             d = {j: "rP"}
    #         else:
    #             d = {j: "rN"}
    #         self.mask_dict.update({i: d})

    # def get_board(self, player):
    #     matrix = self.board.matrix
    #     visible_board = {}
    #     for i in range(self.board.height):
    #         for j in range(self.board.width):
    #             if (i, j) in player.submarine.vision_scope():
    #                 if matrix[i][j]:
    #                     d = {j: self.encode(matrix[i][j], player, i, j)}
    #                     visible_board.update({i: d})
    #             elif (i, j) in player.submarine.radar_scope():
    #                 if matrix[i][j]:
    #                     d = {j: "rP"}
    #                 else:
    #                     d = {j: "rN"}
    #                 visible_board.update({i: d})

    def update(self):
        new_visible_cells = self.player.submarine.get_vision_scope()

        for cell in self.visible_cells:
            if not cell in new_visible_cells:
                self.__remove(cell)
                self.visible_cells.remove(cell)

        for cell in new_visible_cells:
            self.__set_cell_visible(cell)

    def get_radar_pulse(self):
        self.__clean_radar()

        vision_scope = self.player.submarine.get_vision_scope()
        radar_scope = self.player.submarine.get_radar_scope()

        for pos in radar_scope:
            if not pos in vision_scope:
                x, y = pos
                code = self.__encode(self.board[x][y], x, y, radar=True)
                self.__add(pos, code)
                self.radar_cells.append(pos)

    def __add(self, pos, code):
        x, y = pos
        if x in self.mask_dict.keys():
            self.mask_dict[x].update({y: code})
        else:
            self.mask_dict.update({x: {y: code}})

    def __remove(self, pos):
        x, y = pos
        self.mask_dict[x].pop(y)
        if self.mask_dict[x] == {}:
            self.mask_dict.pop(x)

    def __clean_radar(self):
        for pos in self.radar_cells:
            self.__remove(pos)
        self.radar_cells.clear()

    def __set_cell_visible(self, cell):
        x, y = cell
        code = self.__encode(self.board[x][y], x, y)
        self.__add(cell, code)
        if not cell in self.visible_cells:
            self.visible_cells.append(cell)

    def __encode(self, obj, i, j, radar=False):
        # RADAR
        if radar:
            if obj:
                return "rP"
            else:
                return "rN"

        # VISIBLE

        if not obj:
            return "_"

        str = ""
        if obj.player is self.player:
            str += "F"
        else:
            str += "E"

        if isinstance(obj, Submarine):
            if (i, j) == obj.get_head_position():
                str += "H"
            else:
                str += "T"

        elif isinstance(obj, Torpedo):
            str += "To"

        str += str(obj.direction)
        return str
