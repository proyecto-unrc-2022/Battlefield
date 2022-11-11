from app import db
from app.models.user import User
from app.daos.user_dao import *
from app.daos.infantry.infantry_dao import *
from app.models.infantry.projectile_infantry import Projectile_infantry
from app.models.infantry.figure_infantry import Figure_infantry
from app.models.infantry.game_Infantry import Game_Infantry


def test_new_game():
    db.create_all()
    user1 = add_user("ignacio", "123", "@ignacio")
    user2 = add_user("jose", 321, "@jose")
    user3 = add_user("axel", 111, "@axel")
    game = create_game(user1.id)
    #game_1 = Game_Infantry(id_user1=1, id_user2=3)
    #soldier1 = Figure_infantry(id_user="3", id_game="1", hp="10", velocidad="5", tamaño="1", direccion="90", pos_x="5", pos_y="8", type="1")
    #db.session.add_all([user1, user2, user3, game_1, soldier1])
    #db.session.commit()
#
    soldado = Figure_infantry.query.filter_by(id_user= 3).first()
    game1 = Game_Infantry.query.filter_by(id = 1).first()
#
    assert soldado.id_user == user3.id
    assert soldado.id_game == game1.id


