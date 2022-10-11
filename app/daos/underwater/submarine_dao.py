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


def update_position(submarine, x_coord=None, y_coord=None, direction=None):
    if x_coord:
        submarine.x_position = x_coord
    if y_coord:
        submarine.y_position = y_coord
    if direction:
        submarine.direction = direction
    db.session.commit()


def get_submarine(id):
    return db.session.query(Submarine).where(Submarine.id == id).one_or_none()
