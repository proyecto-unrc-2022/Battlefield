from app import db
from app.underwater.models import UnderGame

game_cache = {}


class UnderGameDAO:
    def create(self, host, visitor=None, height=10, width=20):
        game = UnderGame(host=host, visitor=visitor, height=height, width=width)
        self.save(game)
        game.build_board()
        game_cache.update({game.id: game})
        return game

    def get_by_id(self, game_id):
        if game_id in game_cache.keys():
            game = game_cache[game_id]
        else:
            game = db.session.get(UnderGame, game_id)
            if game:
                game.build_board()

        return game

    def save(self, game):
        db.session.add(game)
        db.session.commit()


game_dao = UnderGameDAO()
