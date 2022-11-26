import json

from sqlalchemy.orm import backref, reconstructor, relationship

from app import db
from app.underwater.board.board_mask import BoardMask
from app.underwater.board.under_board import UnderBoard
from app.underwater.game_state import GameState

from ..daos.submarine_dao import submarine_dao
from .submarine import Submarine
from .torpedo import Torpedo


class UnderGame(db.Model):
    __tablename__ = "under_game"
    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    visitor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

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
    winner = relationship("User", foreign_keys=[winner_id])

    submarines = relationship("Submarine", back_populates="game", cascade="all, delete")
    deleted_submarines = relationship("Submarine", cascade="all, delete")
    torpedos = relationship("Torpedo", back_populates="game", cascade="all, delete")
    deleted_torpedos = relationship("Torpedo", cascade="all, delete")

    def __init__(self, host, visitor=None, height=10, width=20):
        self.host = host
        self.visitor = visitor
        self.height = height
        self.width = width
        self.state = GameState.PREGAME
        self.build_board()

    @reconstructor
    def init_on_load(self):
        self.build_board()

    def build_board(self):
        self.board = UnderBoard.build_from(self)

    @staticmethod
    def get_options():
        with open("app/underwater/options.json") as f:
            options = json.load(f)
        return options

    @staticmethod
    def get_submarine_option(option_id):
        options = UnderGame.get_options()
        choosen = options[str(option_id)]
        return choosen

    def is_ongoing(self):
        return self.state == GameState.ONGOING

    def is_finished(self):
        return self.state == GameState.FINISHED

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

        # sub = submarine_dao.create(self, player, sub_stats)
        sub = Submarine(self, player, sub_stats)
        self.place(sub, x_coord, y_coord, direction)
        BoardMask(self, sub)

        if len(self.submarines) == 2:
            self.set_state(GameState.ONGOING)

        self.update_visibilites()
        return sub

    def place(self, obj, x_position, y_position, direction):
        if obj.is_placed():
            raise Exception("object is already placed")

        obj.x_position = x_position
        obj.y_position = y_position
        obj.direction = direction
        self.board.place_object(obj)

    def rotate_object(self, obj, direction):
        if self.is_finished() or direction == obj.direction:
            return

        new_cells = obj.get_tail_positions(direction=direction)
        found_objects = self.board.objects_in_positions(new_cells)
        for other in found_objects:
            if self.is_ongoing():
                self.solve_conflict(obj, other)

        if obj.in_game():
            self.board.clear_all(obj.get_positions())
            obj.direction = direction
            self.board.place_object(obj)

        self.update_visibilites()

    def advance_object(self, obj, n=None):
        if isinstance(obj, Torpedo):
            n = obj.speed

        if n > obj.speed:
            raise Exception("Speed (%s) exceeded" % obj.speed)

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
            obj.x_position = x
            obj.y_position = y

        self.update_visibilites()

    def __destroy_object(self, obj):
        if obj.is_placed():
            self.board.clear_all(obj.get_positions())

        if isinstance(obj, Torpedo):
            self.torpedos.remove(obj)
            self.deleted_torpedos.append(obj)

        elif isinstance(obj, Submarine):
            self.submarines.remove(obj)
            self.deleted_submarines.append(obj)
            if len(self.submarines) < 2:
                self.set_state(GameState.FINISHED)
                self.winner = self.submarines[0].player

    def attack(self, sub):
        next_cell = sub.get_next_position()

        if self.board.valid(next_cell) and self.is_ongoing():
            new_torpedo = sub.create_torpedo()

            if not self.board.is_empty(next_cell):
                self.solve_conflict(new_torpedo, self.board.get_cell_content(next_cell))

            elif self.board.valid(next_cell):
                self.board.place(new_torpedo, next_cell)
                new_torpedo.x_position, new_torpedo.y_position = next_cell
                new_torpedo.direction = sub.direction

            self.update_visibilites()

    def send_radar_pulse(self, sub):
        sub.under_board_mask.get_radar_pulse()
        for s in self.submarines:
            if not sub.player is s.player:
                s.under_board_mask.return_radar_pulse(sub.under_board_mask)

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
        sub1_h = collider.health
        sub2_h = collided.health

        collider.health = max(0, sub1_h - sub2_h)
        collided.health = max(0, sub2_h - sub1_h)

        loser = collider if collider.health == 0 else collided
        self.__destroy_object(loser)

    def __solve_submarine_torpedo(self, sub, tor):
        new_health = sub.health - tor.damage
        sub.health = max(0, new_health)
        self.__destroy_object(tor)
        if sub.health == 0:
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

    def update_visibilites(self):
        for sub in self.submarines:
            sub.update_visibility()
