from app import db
from app.models.underwater.under_models import Submarine, boards


def create_submarine(
    game_id,
    player_id,
    name,
    size,
    speed,
    visibility,
    radar_scope,
    health,
    torpedo_speed,
    torpedo_damage,
    x_position=None,
    y_position=None,
    direction=None,
):
    sub = Submarine(
        game_id=game_id,
        player_id=player_id,
        name=name,
        size=size,
        speed=speed,
        visibility=visibility,
        radar_scope=radar_scope,
        health=health,
        torpedo_speed=torpedo_speed,
        torpedo_damage=torpedo_damage,
    )
    if x_position:
        sub.x_position = x_position
    if y_position:
        sub.y_position = y_position
    if direction:
        sub.direction = direction
    db.session.add(sub)
    db.session.commit()
    return sub


def is_placed(submarine):
    return submarine.x_position or submarine.y_position or submarine.direction


def place_submarine(submarine, x_coord, y_coord, direction):
    if is_placed(submarine):
        raise Exception("submarine is already placed")

    board = boards[submarine.game.id]

    # if not board.segment_is_empty(x_coord, y_coord, direction, submarine.size):
    #     raise Exception("Given position is not available")
    try:
        board.place(submarine, x_coord, y_coord, direction, submarine.size)
    except Exception as e:
        raise Exception("%s" % str(e))

    submarine.x_position = x_coord
    submarine.y_position = x_coord
    submarine.direction = direction

    db.session.commit()


def get_submarine(id):
    return db.session.query(Submarine).where(Submarine.id == id).one_or_none()
