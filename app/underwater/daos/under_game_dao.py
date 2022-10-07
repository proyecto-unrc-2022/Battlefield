from app import db
from app.models.user import User
from app.underwater.models.under_game import UnderGame
from app.underwater.under_board import UnderBoard

from .. import boards


class UnderGameDAO:
    def __init__(self, model):
        self.model = model

    def create(self, host_id, visitor_id=None, height=10, width=20):
        if db.session.query(User).where(User.id == host_id) == None:
            return None

        game = UnderGame(host_id=host_id)
        if visitor_id:
            if db.session.query(User).where(User.id == visitor_id) == None:
                return None
            game.visitor_id = visitor_id

        db.session.add(game)
        db.session.commit()
        boards.update({game.id: UnderBoard(game.id, height, width)})
        return game

    def get_by_id(self, game_id):
        game = db.session.query(UnderGame).where(UnderGame.id == game_id).one_or_none()
        if not game:
            raise ValueError("no game found with id %s" % game_id)
        return game

    def save(self, game):
        db.session.add(game)
        db.session.commit()


game_dao = UnderGameDAO(UnderGame)
