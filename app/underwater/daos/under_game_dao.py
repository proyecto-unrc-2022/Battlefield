from app import db
from app.models.user import User
from app.underwater.models.under_game import UnderGame
from app.underwater.session import sessions
from app.underwater.session.under_game_session import UnderGameSession
from app.underwater.under_board import UnderBoard

from .. import boards


class UnderGameDAO:
    def __init__(self, model):
        self.model = model

    def create(self, host_id, visitor_id=None, height=10, width=20):
        if db.session.query(User).where(User.id == host_id) == None:
            return None

        host = db.session.get(User, host_id)
        visitor = None

        if host.under_game_host or host.under_game_visitor:
            raise Exception("User of id %s is in another game" % host_id)

        game = UnderGame(host=host, height=height, width=width)

        if visitor_id is not None:
            visitor = db.session.get(User, visitor_id)
            if not visitor:
                return None
            game.visitor = visitor

        db.session.add(game)
        db.session.commit()

        boards.pop(game.id, None)
        boards.update({game.id: game.board})
        game.build_board()

        sessions.pop(game.id, None)
        sessions.update({game.id: UnderGameSession(host)})

        if visitor:
            sessions[game.id].add_player(visitor)

        return game

    def get_by_id(self, game_id):
        game = db.session.get(self.model, game_id)
        if game is not None:
            game.build_board()
            if not game.id in sessions:
                sessions.update({game.id: UnderGameSession(game.host)})
                if game.visitor:
                    sessions[game.id].add_player(game.visitor)
        return game

    def save(self, game):
        db.session.add(game)
        db.session.commit()


game_dao = UnderGameDAO(UnderGame)
