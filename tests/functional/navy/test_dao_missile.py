

def test_exist_missile_none(flask_app):
    from app.daos.navy.dynamic_missile_dao import exist_missile, set_missile_in_game
    id_game = 1
    emtpy_missiles = []
    set_missile_in_game(id_game, emtpy_missiles)
    assert exist_missile(id_game, 2, 2) is None

def test_exist_missile_one():
    from app.daos.navy.dynamic_missile_dao import exist_missile, set_missile_in_game

    from app.models.navy.dynamic_missile import DynamicMissile
    id_game = 1
    missile_new = DynamicMissile(
        id_game=1,
        id_ship = 1,
        pos_x=2,
        pos_y=2,
        order=1,
        direction = "N",
        missile_type=1
    )
    one_missiles = [missile_new]
    set_missile_in_game(id_game, one_missiles)
    assert exist_missile(id_game, 2, 2) == missile_new