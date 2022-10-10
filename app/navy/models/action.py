from app import db

class Action(db.Model):

    __tablename__ = "actions"

    id = db.Column(db.Integer, primary_key=True)
    nave_game_id = db.Column(db.Integer)
    ship_id = db.Column(db.Integer)
    course = db.Column(db.String(2))
    move = db.Column(db.Integer(1))
    attack = db.Column(db.Integer(1))
    missile_type_id  = db.Column(db.Integer(1))


    def __init__(self, nave_game_id, ship_id, course, move, attack, missile_type_id, ):
        self.nave_game_id = nave_game_id
        self.ship_id = ship_id
        self.course = course
        self.move = move
        self.attack = attack
        self.missile_type_id = missile_type_id
        



