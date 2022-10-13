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

        host = db.session.get(User, host_id)
        if host.under_game_host or host.under_game_visitor:
            raise Exception("User of id %s is in another game" % host_id)

        game = UnderGame(host_id=host_id, height=height, width=width)
        game.board.id = game.id
        if visitor_id:
            if db.session.query(User).where(User.id == visitor_id) == None:
                return None
            game.visitor_id = visitor_id

        db.session.add(game)
        db.session.commit()
        boards.update({game.id: game.board})
        return game

    def get_by_id(self, game_id):
        return db.session.get(UnderGame, game_id)

    def save(self, game):
        db.session.add(game)
        db.session.commit()


game_dao = UnderGameDAO(UnderGame)
