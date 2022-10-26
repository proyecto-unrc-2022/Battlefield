from app import db


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
        self, navy_game_id, ship_id, course, move, attack, missile_type_id, user_id
    ):
        self.navy_game_id = navy_game_id
        self.ship_id = ship_id
        self.course = course
        self.move = move
        self.attack = attack
        self.missile_type_id = missile_type_id
        self.user_id = user_id
