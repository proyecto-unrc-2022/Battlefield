class UnderBoard:
    def __init__(self, id, height=10, width=20):
        self.id = id
        self.height = height
        self.width = width
        self.matrix = []
        for i in range(height):
            self.matrix.append([None] * width)

    def valid(self, x, y):
        return x >= 0 and x < self.height and y >= 0 and y < self.width

    def place(self, obj):
        for (x, y) in obj.get_positions():
            if not self.valid(x, y):
                raise Exception("Invalid coordinates (%s,%s)" % (x, y))

            if self.matrix[x][y]:
                raise Exception("Position (%s,%s) is not available" % (x, y))

            self.matrix[x][y] = obj

    def get_cell_content(self, x, y):
        if not self.valid(x, y):
            raise ValueError("Invalid coordinates")

        return self.matrix[x][y]

    def cells_are_empty(self, pair_list):
        for (x, y) in pair_list:
            if self.matrix[x][y]:
                return False
        return True

    def clear(self, pair_list):
        for (x, y) in pair_list:
            self.matrix[x][y] = None

    def __str__(self):
        m = self.matrix
        h = len(m)
        w = len(m[0])

        print("-" * (w * 4 + 1))
        for i in range(h):
            print("|", end="")
            for j in range(w):
                if self.matrix[i][j]:
                    o = self.matrix[i][j]
                    if (o.x_position, o.y_position) == (i, j):
                        print(" H |", end="")
                    else:
                        print(" 0 |", end="")
                else:
                    print("   |", end="")
            print("")
        print("-" * (w * 4 + 1))
