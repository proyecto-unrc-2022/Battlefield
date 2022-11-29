from sqlalchemy.orm import relationship

from app import db


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("under_game.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String)
    name = db.Column(db.String)

    game_session_id = db.Column(db.Integer, db.ForeignKey("under_game_session.id"))

    game = relationship("UnderGame")
    player = relationship("User")
    under_game_session = relationship("UnderGameSession")

    __mapper_args__ = {
        "polymorphic_identity": "command",
        "polymorphic_on": type,
    }

    def __init__(self, game, player, **params):
        self.game = game
        self.player = player

    def execute(self):
        raise NotImplementedError()
