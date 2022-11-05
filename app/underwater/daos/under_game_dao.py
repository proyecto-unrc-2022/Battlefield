from app import db
from app.daos.user_dao import get_user_by_id
from app.underwater.models.under_game import UnderGame

# from app.underwater.session import sessions
# from app.underwater.session.under_game_session import UnderGameSession

game_cache = {}


class UnderGameDAO:
    def __init__(self, model):
        self.model = model

    def create(self, host, visitor=None, height=10, width=20):
        if host.under_game_host or host.under_game_visitor:
            raise Exception("User of id %s is in another game" % host.id)

        game = UnderGame(host=host, visitor=visitor, height=height, width=width)

        self.save(game)

        game.build_board()

        game_cache.update({game.id: game})
        return game

    def get_by_id(self, game_id):
        if game_id in game_cache.keys():
            game = game_cache[game_id]
        else:
            game = db.session.get(self.model, game_id)
            if game:
                game.build_board()

        db.session.add(game)
        return game

    def save(self, game):
        db.session.add(game)
        db.session.commit()


game_dao = UnderGameDAO(UnderGame)
