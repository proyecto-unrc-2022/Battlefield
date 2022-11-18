from app import db
from sqlalchemy import event
from sqlalchemy.orm import Session

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

@event.listens_for(Action, 'after_insert')
def receive_after_create(mapper, connection, target):
    from app.navy.services.navy_game_service import navy_game_service
    navy_game_id = target.navy_game_id
    if navy_game_service.should_update(navy_game_id):
            navy_game_service.play_round(navy_game_id)
    


""" @event.listens_for(Action, 'after_commit')
def receive_after_commit(Session):
    return """


""" @event.listens_for(Action, 'after_create')
def create_version(target, connection, **kw):
    id = target.navy_game_id
    transaction = connection.begin()
    # do something with the transaction, or the connection...
    transaction.commit() """


""" @event.listens_for(Action, "actions", propagate=True)
def instrument_class(mapper, class_):
    if mapper.local_table is not None:
        trigger_for_table(mapper.local_table)

def trigger_for_table(table):
    trig_ddl = ""
    event.listen(table, 'after_create', trig_ddl) """
