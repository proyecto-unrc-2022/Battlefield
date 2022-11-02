import json

from sqlalchemy.orm import backref, relationship

from app import db
from app.daos.user_dao import get_user_by_id
from app.underwater.daos.under_game_dao import game_dao

from ..command import Command, SubmarineCommand


class UnderGameSession(db.Model):
    __tablename__ = "under_game_session"
    id = db.Column(db.Integer, primary_key=True)
    turn = db.Column(db.Integer)
    order = db.Column(db.Integer)
    host_moved = db.Column(db.Boolean, default=False)
    visitor_moved = db.Column(db.Boolean, default=False)

    game_id = db.Column(db.Integer, db.ForeignKey("under_game.id"))
    host_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    visitor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    game = relationship("UnderGame")
    host = relationship("User", foreign_keys=host_id)
    visitor = relationship("User", foreign_keys=visitor_id)

    commands = relationship("Command", backref="under_game_session")

    def __init__(self, game, host, visitor=None):
        self.game = game
        self.host = host
        self.visitor = visitor
        self.turn = 0  # 0 is host, 1 is visitor
        self.order = 1  # 1 means forward, -1 means backward

    @staticmethod
    def start_session_for(game):
        new_session = UnderGameSession(game, game.host, game.visitor)

        db.session.add(new_session)
        db.session.commit()
        return new_session

    def add_command(self, c):
        self.commands.append(c)

    def next_turn(self):
        self.turn += self.order
        self.turn = self.turn % 1

    def execute_commands(self):
        for c in self.commands:
            c.execute()
        self.commands.clear()

    def invert_order(self):
        self.__order *= -1

    def everyone_moved(self):
        return self.host_moved and self.visitor_moved

    def current_turn_player(self):
        return self.host if self.turn == 0 else self.visitor

    def clear(self):
        self.turn = 0
        self.order = 1
        self.commands.clear()

    def to_dict(self):
        # commands_to_dict = []  esto iria?
        # i = 1
        # for c in self.__commands:
        #     commands_to_dict.update({"{}".format(i): c.__repr__()})
        #     i += 1
        dict = {
            "turn": self.__turn,
            "order": self.__order  # ,
            # "commands": commands_to_dict,
            # "game": self.game.to_dict
            # "remaining_to_move" lo ponemos?
        }
        dict.update(self.game.to_dict())  # append game dict to this dict
        return dict

    def __repr__(self):
        return json.dumps(self.to_dict())
