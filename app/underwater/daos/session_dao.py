from app import db
from app.underwater.session.under_game_session import UnderGameSession


class SessionDAO:
    def create(self, game, host, visitor=None):
        session = UnderGameSession(game, host, visitor)
        db.session.add(session)
        db.session.commit()
        return session

    def start_session_for(self, game):
        return self.create(game, game.host, game.visitor)

    def get_by_id(self, sid):
        return db.session.get(UnderGameSession, sid)

    def get_all(self):
        return UnderGameSession.query.all()

    def delete(self, sid):
        UnderGameSession.query.filter_by(id=sid).delete()
        db.session.commit()

    def save(self, session):
        db.session.add(session)
        db.session.commit()


session_dao = SessionDAO()
