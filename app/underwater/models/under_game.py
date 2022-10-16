import json

from sqlalchemy.orm import backref, relationship

from app import db
from app.models.user import User
from app.underwater import boards
from app.underwater.game_state import GameState
from app.underwater.models.submarine import Submarine
from app.underwater.models.submerged_object import SubmergedObject
from app.underwater.models.torpedo import Torpedo
from app.underwater.under_board import UnderBoard

from ..daos.submarine_dao import submarine_dao


class UnderGame(db.Model):
    __tablename__ = "under_game"
    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey(User.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    state = db.Column(db.Integer)

    host = relationship(
        "User",
        backref=backref("under_game_host", uselist=False),
        foreign_keys=[host_id],
    )
    visitor = relationship(
        "User",
        backref=backref("under_game_visitor", uselist=False),
        foreign_keys=[visitor_id],
    )

    submarines = relationship("Submarine", back_populates="game")
    torpedos = relationship("Torpedo", back_populates="game")

    def __init__(self, host_id, height=10, width=20):
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

    def is_ongoing(self):
        return self.state == GameState.ONGOING

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

        for sub in self.submarines:
            if sub.player_id == player_id:
                raise Exception("Player already has a submarine")

        sub = submarine_dao.create_submarine(self.id, player_id, sub_stats)
        self.place(sub, x_coord, y_coord, direction)
        if len(self.submarines) == 2:
            self.state = GameState.ONGOING
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
        for sub in self.submarines + self.torpedos:
            if isinstance(sub, model):
                ret_list.append(sub)
        return ret_list

    def get_submarines(self):
        return self.submarines

    def get_torpedos(self):
        return self.torpedos

    def rotate_object(self, obj, direction):
        if direction == obj.direction:
            return

        new_cells = obj.get_tail_positions(direction=direction)
        found_objects = self.board.objects_in_positions(new_cells)
        for other in found_objects:
            if self.is_ongoing():
                self.solve_conflict(obj, other)

        if obj.in_game():
            self.board.clear_all(obj.get_positions())
            obj.set_position(direction=direction)
            self.board.place_object(obj)

    # def advance_object(self, obj, n=None):
    #     if type(obj) is Submarine:
    #         self.__advance_submarine(obj, n)
    #     else:
    #         self.__advance_torpedo(obj)

    def advance_object(self, obj, n=None):
        if isinstance(obj, Torpedo):
            n = obj.get_speed()

        if n > obj.get_speed():
            raise Exception("Speed (%s) exceeded" % obj.get_speed())

        while n > 0 and self.is_ongoing() and obj.in_game():
            if self.board.valid(obj.get_next_position()):
                self.__advance_object_one(obj)
                n -= 1
            else:
                self.__destroy_object(obj)
                break

    # def __advance_submarine(self, sub, n):
    #     if n > sub.get_speed():
    #         raise Exception("Speed (%s) exceeded" % sub.get_speed())

    #     while n > 0 and self.is_ongoing():
    #         if not self.board.valid(sub.get_next_position()):
    #             break
    #         self.__advance_object_one(sub)
    #         n -= 1

    # def __advance_torpedo(self, torp):
    #     n = torp.get_speed()
    #     while n > 0 and self.is_ongoing():
    #         if self.board.valid(torp.get_next_position()):
    #             self.__advance_object_one(torp)
    #         else:
    #             self.__destroy_torpedo(torp)
    #             break

    def __advance_object_one(self, obj):
        x, y = next_cell = obj.get_next_position()

        if not self.board.is_empty(next_cell):
            self.solve_conflict(obj, self.board.get_cell_content(next_cell))

        if self.is_ongoing() and obj.in_game():
            self.board.clear(obj.get_last_position())
            self.board.place(obj, next_cell)
            obj.set_position(x_position=x, y_position=y)

    def __destroy_object(self, obj):
        self.board.clear_all(obj.get_positions())

        if isinstance(obj, Torpedo):
            self.torpedos.remove(obj)

        elif isinstance(obj, Submarine):
            self.submarines.remove(obj)
            if len(self.get_submarines()) < 2:
                self.set_state(GameState.FINISHED)

    def attack(self, sub):
        next_cell = sub.get_next_position()

        new_torpedo = sub.create_torpedo()

        if not self.board.is_empty(next_cell):
            self.solve_conflict(new_torpedo, self.board.get_cell_content(next_cell))
        elif self.board.valid(next_cell):
            self.board.place(new_torpedo, next_cell)

    def solve_conflict(self, obj1, obj2):
        # Conflict types = "s-s, s-t, t-t"
        if isinstance(obj1, Submarine):
            if isinstance(obj2, Submarine):
                self.__solve_submarine_crash(obj1, obj2)
            elif isinstance(obj2, Torpedo):
                self.__solve_submarine_torpedo(obj1, obj2)
        elif isinstance(obj1, Torpedo):
            if isinstance(obj2, Submarine):
                self.__solve_submarine_torpedo(obj2, obj1)
            elif isinstance(obj2, Torpedo):
                self.__solve_torpedo_crash(obj1, obj2)

    def __solve_submarine_crash(self, collider=None, collided=None):
        sub1_h = collider.get_health()
        sub2_h = collided.get_health()

        collider.set_health(max(0, sub1_h - sub2_h))
        collided.set_health(max(0, sub2_h - sub1_h))

        loser = collider if collider.get_health() == 0 else collided
        self.__destroy_object(loser)

    def __solve_submarine_torpedo(self, sub, tor):
        new_health = sub.get_health() - tor.get_damage()
        sub.set_health(max(0, new_health))
        self.__destroy_object(tor)
        if sub.get_health() == 0:
            self.__destroy_object(sub)

    def __solve_torpedo_crash(self, tor1, tor2):
        self.__destroy_object(tor1)
        self.__destroy_object(tor2)

    def set_state(self, state):
        self.state = state

    def build_board(self):
        if self.id not in boards.keys():
            board = UnderBoard.build_from(self)
            boards.update({self.id: board})
            self.board = board
        else:
            self.board = boards[self.id]

    def __str__(self):
        return self.board.__str__()
