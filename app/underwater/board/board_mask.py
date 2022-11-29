import json

from sqlalchemy.orm import backref, reconstructor, relationship

from app import db
from app.underwater.models.submarine import Submarine
from app.underwater.models.torpedo import Torpedo


class BoardMask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_mask = db.Column(db.String)
    submarine_id = db.Column(db.Integer, db.ForeignKey("submarine.id"))

    submarine = relationship("Submarine", back_populates="under_board_mask")

    def __init__(self, game, submarine):
        self.submarine = submarine
        self.mask_dict = {}
        self.radar_cells = set()
        self.visible_cells = set()
        self.update()

    @reconstructor
    def retreive_mask(self):
        self.mask_dict = json.loads(self.board_mask)
        self.radar_cells = set()
        self.visible_cells = set()
        for si in self.mask_dict:
            for sj in self.mask_dict[si]:
                i = int(si)
                j = int(sj)
                if self.mask_dict[si][sj][0] == "r":
                    self.radar_cells.add((i, j))
                else:
                    self.visible_cells.add((i, j))

    def update(self):
        new_visible_cells = self.submarine.get_vision_scope()

        for cell in list(
            self.visible_cells
        ):  # Casted to list to allow removal during iteration
            if not cell in new_visible_cells:
                self.__remove(cell)
                self.visible_cells.remove(cell)

        for cell in new_visible_cells:
            self.__set_cell_visible(cell)

        self.save()

    def get_radar_pulse(self):
        self.__clean_radar()

        vision_scope = self.submarine.get_vision_scope()
        radar_scope = self.submarine.get_radar_scope()

        for pos in radar_scope:
            if not pos in vision_scope:
                code = self.__encode(
                    self.submarine.game.board.get_cell_content(pos), pos, radar=True
                )
                self.__add(pos, code)
                self.radar_cells.add(pos)

        self.save()

    def return_radar_pulse(self, enemy_mask):
        my_positions = self.submarine.get_positions()
        enemy_positions = enemy_mask.submarine.get_positions()

        i_was_seen = False
        for pos in my_positions:
            if pos in enemy_mask.radar_cells:
                i_was_seen = True
                break

        if i_was_seen:
            print(enemy_positions)
            print(self.visible_cells)
            for pos in enemy_positions:
                if pos in self.visible_cells:
                    continue
                if pos in self.submarine.get_radar_scope():
                    self.__add(pos, "rP")
                    self.radar_cells.add(pos)

        self.save()

    def __add(self, pos, code):
        x = str(pos[0])
        y = str(pos[1])
        if x in self.mask_dict.keys():
            self.mask_dict[x].update({y: code})
        else:
            self.mask_dict.update({x: {y: code}})

    def __remove(self, pos):
        x = str(pos[0])
        y = str(pos[1])
        self.mask_dict[x].pop(y)
        if self.mask_dict[x] == {}:
            self.mask_dict.pop(x)

    def __clean_radar(self):
        for pos in self.radar_cells:
            self.__remove(pos)
        self.radar_cells.clear()

    def __set_cell_visible(self, cell):
        code = self.__encode(self.submarine.game.board.get_cell_content(cell), cell)
        self.__add(cell, code)
        if not cell in self.visible_cells:
            self.visible_cells.add(cell)
        if cell in self.radar_cells:
            self.radar_cells.remove(cell)

    def __encode(self, obj, pos, radar=False):
        # RADAR
        if radar:
            if obj:
                return "rP"
            else:
                return "rN"

        # VISIBLE

        if not obj:
            return "_"

        s = ""
        if obj.player is self.submarine.player:
            s += "F"
        else:
            s += "E"

        if isinstance(obj, Submarine):
            if pos == obj.get_head_position():
                s += "H"
            else:
                s += "T"

        elif isinstance(obj, Torpedo):
            s += "*"

        s += str(obj.direction)
        return s

    def save(self):
        self.board_mask = json.dumps(self.mask_dict)

    def get_visible_board(self):
        return self.mask_dict
