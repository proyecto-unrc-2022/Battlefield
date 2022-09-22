from app import db
from app.models.user import User


class air_force_game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_a_id = db.Column(db.Integer, db.ForeignKey(User.id))
    player_b_id = db.Column(db.Integer, db.ForeignKey(User.id))
