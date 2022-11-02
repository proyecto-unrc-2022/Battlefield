from app.underwater.models.submarine import Submarine


class UnderBoard:
    def __init__(self, height=10, width=20):
        self.height = height
        self.width = width
        self.matrix = []
        for _ in range(height):
            self.matrix.append([None] * width)

    @staticmethod
    def build_from(game):
        board = UnderBoard(height=game.get_height(), width=game.get_width())
        for obj in game.submarines + game.torpedos:
            for (x, y) in obj.get_positions():
                board.matrix[x][y] = obj
        return board

    def valid(self, p):
        x, y = p
        return x >= 0 and x < self.height and y >= 0 and y < self.width

    def place(self, obj, pos):
        x, y = pos
        if not self.valid(pos):
            raise Exception("Invalid coordinates (%s,%s)" % (x, y))
        self.matrix[x][y] = obj

    def place_object(self, obj):
        self.place(obj, obj.get_head_position())
        for pos in obj.get_tail_positions():
            if self.valid(pos):
                self.place(obj, pos)

    def get_cell_content(self, p):
        if not self.valid(p):
            raise ValueError("Invalid coordinates")

        x, y = p
        return self.matrix[x][y]

    def is_empty(self, pos):
        x, y = pos

        if not self.valid(pos):
            raise Exception("Invalid coordinates (%s,%s)" % (x, y))

        return False if self.matrix[x][y] else True

    def cells_are_empty(self, pair_list):
        for pos in pair_list:
            if not self.is_empty(pos):
                return False
        return True

    def clear_all(self, pair_list):
        for (x, y) in pair_list:
            if self.valid((x, y)):
                self.matrix[x][y] = None

    def clear(self, p):
        if self.valid(p):
            x, y = p
            self.matrix[x][y] = None

    def __str__(self):
        m = self.matrix
        h = self.height
        w = self.width

        str = ""
        str += "-" * (w * 4 + 1) + "\n"
        for i in range(h):
            str += "|"
            for j in range(w):
                if self.matrix[i][j]:
                    o = self.matrix[i][j]
                    if (o.x_position, o.y_position) == (i, j):
                        if type(o) is Submarine:
                            str += " %s |" % o.player.id
                        else:
                            str += " * |"
                    else:
                        str += " 0 |"
                else:
                    str += "   |"
            str += "\n"
        str += ("-" * (w * 4 + 1)) + "\n"
        return str

    def objects_in_positions(self, pos_list):
        ret_list = []
        for (x, y) in pos_list:
            if (
                self.valid((x, y))
                and self.matrix[x][y]
                and self.matrix[x][y] not in ret_list
            ):
                ret_list.append(self.matrix[x][y])
        return ret_list
