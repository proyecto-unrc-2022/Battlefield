from app import db
from app.models.user import User
from app.models.infantry.infantry_game import Game_Infantry, Figure_infantry, Projectile

def test_new_game():
    db.create_all()
    user1 = User(username="ignacio", email="@ignacio", password="123")
    user2 = User(username="jose", email="@jose", password="321")
    user3 = User(username="axel", email="@axel", password="111")
    game_1 = Game_Infantry(id_user1=1, id_user2=3)
    soldier1 = Figure_infantry(id_user="3", id_game="1", hp="10", velocidad="5", tamaño="1", direccion="90", pos_x="5", pos_y="8", type="1")
    db.session.add_all([user1, user2, user3, game_1, soldier1])
    db.session.commit()

    soldado = Figure_infantry.query.filter_by(id_user= 3).first()
    game1 = Game_Infantry.query.filter_by(id = 1).first()

    assert soldado.id_user == user3.id
    assert soldado.id_game == game1.id
