import json

from sqlalchemy.orm import relationship

from app import db


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

    def add_visitor(self, visitor):
        self.visitor = visitor
        self.game.visitor = visitor

    def add_command(self, c):
        self.commands.append(c)
        db.session.add(c)
        if c.player is self.host:
            self.host_moved = True
        else:
            self.visitor_moved = True

    def next_turn(self):
        self.turn += self.order
        self.turn = self.turn % 2

    def execute_commands(self):
        for c in self.commands:
            c.execute()
        self.commands.clear()
        self.host_moved = False
        self.visitor_moved = False

    def invert_order(self):
        self.order *= -1

    def everyone_moved(self):
        return self.host_moved and self.visitor_moved

    def current_turn_player(self):
        return self.host if self.turn == 0 else self.visitor

    def clear(self):
        self.turn = 0
        self.order = 1
        self.commands.clear()

    def to_dict(self):
        return {
            "turn": self.turn,
            "order": self.order,
            "host_id": self.host_id,
            "visitor_id": self.visitor_id,
            "game_state": self.game.state,
        }

    def get_visible_state(self, player):
        d = {
            "session_id": self.id,
            "game_id": self.game.id,
            "host_id": self.host_id,
            "visitor_id": self.visitor_id,
            "turn": self.turn,
            "order": self.order,
        }
        # Show submarine only if it exists
        if player.submarine:
            d.update(
                {
                    "submarine": player.submarine.to_dict(),
                    "visible_board": player.submarine.under_board_mask.get_visible_board(),
                }
            )
        return d

    def has_player(self, player):
        return self.host is player or self.visitor is player
