import json

from sqlalchemy.orm import relationship

from app import db
from app.models.user import User
from app.underwater import boards
from app.underwater.game_state import GameState
from app.underwater.models.submarine import Submarine
from app.underwater.models.submerged_object import SubmergedObject
from app.underwater.models.torpedo import Torpedo
from app.underwater.under_board import UnderBoard

from ..daos.submarine_dao import sub_dao


class UnderGame(db.Model):
    __tablename__ = "under_game"
    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    state = db.Column(db.Integer)

    host = relationship("User", backref="under_game_host", foreign_keys=[host_id])
    visitor = relationship(
        "User", backref="under_game_visitor", foreign_keys=[visitor_id]
    )

    submerged_objects = relationship("SubmergedObject", back_populates="game")

    def __init__(self, host_id, height=10, width=20):
        self.board = UnderBoard(self.id, height, width)
        self.host_id = host_id
        self.height = height
        self.width = width
        self.state = GameState.PREGAME

    # submarines = relationship("Submarine", back_populates="game")
    # torpedos = relationship("Torpedo", back_populates="game")

    @staticmethod
    def get_options():
        options_json = open("app/underwater/options.json")
        options = json.load(options_json)
        return options

    @staticmethod
    def get_submarine_option(option_id):
        options = UnderGame.get_options()

        try:
            choosen = options[str(option_id)]
        except Exception:
            return None

        return choosen

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def has_user(self, player_id):
        return self.host_id == player_id or self.visitor_id == player_id

    def add_submarine(self, player_id, option_id, x_coord, y_coord, direction):
        sub_stats = UnderGame.get_submarine_option(option_id)

        if not self.has_user(player_id):
            raise ValueError("the game does not have the specified player")

        for obj in self.submerged_objects:
            if obj.player_id == player_id:
                raise Exception("Player already has a submarine")

        sub = sub_dao.create_submarine(self.id, player_id, sub_stats)
        self.place(sub, x_coord, y_coord, direction)
        return sub

    def place(self, obj, x_coord, y_coord, direction):
        if obj.is_placed():
            raise Exception("submarine is already placed")

        obj.set_position(x_coord, y_coord, direction)
        self.board.place_object(obj)

    def contains_object(self, obj_id):
        for obj in self.submerged_objects:
            if obj.id == obj_id:
                return True
        return False

    def get_id(self):
        return self.id

    def get_host(self):
        return self.host

    def get_visitor(self):
        return self.visitor

    def get_submerged_objects(self, model=SubmergedObject):
        ret_list = []
        for obj in self.submerged_objects:
            if isinstance(obj, model):
                ret_list.append(obj)
        return ret_list

    def get_submarines(self):
        return self.get_submerged_objects(Submarine)

    def get_torpedos(self):
        return self.get_submerged_objects(Torpedo)

    def rotate_object(self, obj, direction):
        if direction == obj.direction:
            return

        new_cells = obj.get_tail_positions(direction=direction)
        found_objects = self.board.objects_in_positions(new_cells)
        if found_objects:
            self.run_conflict(obj, found_objects[0])

        if not self.state == GameState.FINISHED:
            self.board.clear_all(obj.get_positions())
            obj.set_position(direction=direction)
            sub_dao.save(obj)
            self.board.place_object(obj)

    def advance_object_one(self, obj):
        next_cell = obj.get_next_position()
        x, y = next_cell

        if not self.board.valid(next_cell):
            raise Exception("Object cannot move forward")

        if not self.board.is_empty(next_cell):
            self.run_conflict(obj, self.board.get_cell_content(next_cell))

        if not self.state == GameState.FINISHED:
            old_cells = obj.get_positions()
            self.board.clear(old_cells[-1])
            self.board.place(obj, next_cell)
            obj.set_position(x_position=x, y_position=y)

    def attack(self, sub):
        next_cell = sub.get_next_position()

        if not self.board.valid(next_cell):
            return  # Que hacemos en este caso??

        new_torpedo = sub.create_torpedo()

        if not self.board.is_empty(next_cell):
            self.run_conflict(new_torpedo, self.board.get_cell_content(next_cell))
        else:
            self.board.place(new_torpedo, next_cell)
