from app import create_app
from app.models.user import User
from app.models.navy.dynamic_game import Game
from app.models.navy.dynamic_ship import DynamicShip

app = create_app()
#use context
with app.app_context():
    db = app.db
    db.drop_all()
    db.create_all()

    u = User("juan","123","email@email.com")
    db.session.add(u)
    db.session.commit()

    g = Game()

    g.id_user_1 = u.id
    db.session.add(g)
    db.session.commit()

    ship2 = DynamicShip(
        id_game=g.id,
        id_user=u.id,
        hp=120,
        direction="N",
        pos_x=2,
        pos_y=2,
        ship_type="1",
    )

    db.session.add(ship2)
    db.session.commit()





