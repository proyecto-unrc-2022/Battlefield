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

    def __init__(self, host, visitor=None, height=10, width=20):
        self.host = host
        if visitor:
            self.visitor = visitor
        self.height = height
        self.width = width
        self.state = GameState.PREGAME
        self.submarines = []
        self.torpedos = []
        self.build_board()

    def build_board(self):
        self.board = UnderBoard.build_from(self)

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

    def is_finished(self):
        return self.state == GameState.FINISHED

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_id(self):
        return self.id

    def get_host(self):
        return self.host

    def get_visitor(self):
        return self.visitor

    def get_submarines(self):
        return self.submarines

    def get_torpedos(self):
        return self.torpedos

    def has_user(self, player):
        return self.host is player or self.visitor is player

    def add_submarine(self, player, option_id, x_coord, y_coord, direction):
        sub_stats = UnderGame.get_submarine_option(option_id)
        if self.is_finished():
            return Exception("the game has already finished")

        if not self.has_user(player):
            raise ValueError("the game does not have the specified player")

        for sub in self.submarines:
            if sub.player is player:
                raise Exception("player already has a submarine")

        sub = Submarine(self, player, sub_stats)
        self.place(sub, x_coord, y_coord, direction)

        if len(self.submarines) == 2:
            self.set_state(GameState.ONGOING)
        return sub

    def place(self, obj, x_coord, y_coord, direction):
        if obj.is_placed():
            raise Exception("object is already placed")

        obj.set_position(x_coord, y_coord, direction)
        self.board.place_object(obj)

    def rotate_object(self, obj, direction):
        if direction == obj.direction:
            return
        if self.is_finished():
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

    def advance_object(self, obj, n=None):
        if isinstance(obj, Torpedo):
            n = obj.get_speed()

        if n > obj.get_speed():
            raise Exception("Speed (%s) exceeded" % obj.get_speed())

        while n > 0 and self.is_ongoing() and obj.in_game():
            self.__advance_object_one(obj)
            n -= 1

    def __advance_object_one(self, obj):
        x, y = next_cell = obj.get_next_position()

        if not self.board.valid(next_cell):
            self.__destroy_object(obj)

        elif not self.board.is_empty(next_cell):
            self.solve_conflict(obj, self.board.get_cell_content(next_cell))

        if obj.in_game():
            self.board.clear(obj.get_last_position())
            self.board.place(obj, next_cell)
            obj.set_position(x_position=x, y_position=y)

    def __destroy_object(self, obj):
        if obj.is_placed():
            self.board.clear_all(obj.get_positions())

        if isinstance(obj, Torpedo):
            self.torpedos.remove(obj)

        elif isinstance(obj, Submarine):
            self.submarines.remove(obj)
            if len(self.get_submarines()) < 2:
                self.set_state(GameState.FINISHED)

    def attack(self, sub):
        x, y = next_cell = sub.get_next_position()

        if self.board.valid(next_cell) and self.is_ongoing():
            new_torpedo = sub.create_torpedo()

            if not self.board.is_empty(next_cell):
                self.solve_conflict(new_torpedo, self.board.get_cell_content(next_cell))

            elif self.board.valid(next_cell):
                self.board.place(new_torpedo, next_cell)
                new_torpedo.set_position(x, y, sub.get_direction())

    def solve_conflict(self, obj1, obj2):
        # Conflict types = "s-s, s-t, t-t"
        if isinstance(obj1, Submarine):
            if isinstance(obj2, Submarine):
                self.__solve_submarines_crash(obj1, obj2)
            elif isinstance(obj2, Torpedo):
                self.__solve_submarine_torpedo(obj1, obj2)
        elif isinstance(obj1, Torpedo):
            if isinstance(obj2, Submarine):
                self.__solve_submarine_torpedo(obj2, obj1)
            elif isinstance(obj2, Torpedo):
                self.__solve_torpedos_crash(obj1, obj2)

    def __solve_submarines_crash(self, collider=None, collided=None):
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

    def __solve_torpedos_crash(self, tor1, tor2):
        self.__destroy_object(tor1)
        self.__destroy_object(tor2)

    def set_state(self, state):
        self.state = state

    def __str__(self):
        return self.board.__str__()

    def to_dict(self):
        submarines_as_dicts = []
        torpedos_as_dicts = []
        for sub in self.submarines:
            submarines_as_dicts.append(sub.to_dict())
        for tor in self.torpedos:
            torpedos_as_dicts.append(tor.to_dict())
        dict = {
            "id": self.id,
            "host_id": self.host_id,
            "visitor_id": self.visitor_id,
            "height": self.height,
            "width": self.width,
            "state": self.state,
            "submarines": submarines_as_dicts,
            "torpedos": torpedos_as_dicts,
        }
        return dict

    def __repr__(self):
        return json.dumps(self.to_dict())
