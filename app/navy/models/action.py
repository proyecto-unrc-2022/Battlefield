from sqlalchemy import event

from app import db, io
from app.navy.dtos.navy_game_state_dto import NavyGameStateDTO


class Action(db.Model):

    __tablename__ = "actions"

    id = db.Column(db.Integer, primary_key=True)
    navy_game_id = db.Column(db.Integer(), db.ForeignKey("navy_games.id"))
    ship_id = db.Column(db.Integer)
    course = db.Column(db.String(2))
    move = db.Column(db.Integer())
    attack = db.Column(db.Boolean())
    missile_type_id = db.Column(db.Integer())
    round = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __init__(
        self,
        navy_game_id,
        ship_id,
        course,
        move,
        attack,
        missile_type_id,
        user_id,
        round,
    ):
        self.navy_game_id = navy_game_id
        self.ship_id = ship_id
        self.course = course
        self.move = move
        self.attack = attack
        self.missile_type_id = missile_type_id
        self.user_id = user_id
        self.round = round


@event.listens_for(db.session, "before_commit")
def before_commit(session):
    for obj in db.session:
        if isinstance(obj, Action):
            from app.navy.services.navy_game_service import navy_game_service

            if navy_game_service.should_update(obj.navy_game_id):
                navy_game_service.play_round(obj.navy_game_id)

                """navy_game = navy_game_service.get_by_id(obj.navy_game_id)
                io.send(NavyGameStateDTO(navy_game.id,navy_game.user1_id).dump(),broadcast=True,to=navy_game.user1_id)
                io.send(NavyGameStateDTO(navy_game.id,navy_game.user2_id).dump(),broadcast=True,to=navy_game.user2_id) """
