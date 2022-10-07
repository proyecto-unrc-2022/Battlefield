class UnderBoard:
    def __init__(self, id, height=10, width=20):
        self.id = id
        self.height = height
        self.width = width
        self.matrix = []
        for i in range(height):
            self.matrix.append([None] * width)

    @staticmethod
    def move_pointer(x, y, direction):
        d = direction % 8
        if d == 0:
            return x - 1, y
        elif d == 1:
            return x - 1, y + 1
        elif d == 2:
            return x, y + 1
        elif d == 3:
            return x + 1, y + 1
        elif d == 4:
            return x + 1, y
        elif d == 5:
            return x + 1, y - 1
        elif d == 6:
            return x, y - 1
        elif d == 7:
            return x - 1, y - 1
        else:
            raise TypeError("direction must be an integer")

    def valid(self, x, y):
        return x >= 0 and x < self.height and y >= 0 and y < self.width

    def place(self, obj, x_coord, y_coord, direction, size=1):
        i = size
        x = x_coord
        y = y_coord
        d = direction

        if not self.valid(x_coord, y_coord):
            raise Exception("Invalid coordinates")

        if not self.segment_is_empty(x, y, d, i):
            raise Exception("Given position is not available")

        while i > 0 and self.valid(x, y):
            self.matrix[x][y] = obj
            x, y = self.move_pointer(x, y, d + 4)  # +4 inverts the direction
            i = i - 1

    def get_cell_content(self, x, y):
        if not self.valid(x, y):
            raise ValueError("Invalid coordinates")

        return self.matrix[x][y]

    def segment_is_empty(self, x_coord, y_coord, direction=0, length=1):
        d = direction % 8
        i = length
        x = x_coord
        y = y_coord

        while i > 0 and self.valid(x, y):
            if self.get_cell_content(x, y):
                return False
            x, y = self.move_pointer(x, y, d)
            i = i - 1

        return True

