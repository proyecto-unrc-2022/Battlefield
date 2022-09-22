from sqlalchemy import update

from app import db
from app.models.airforce.plane import Plane


def add_plane(name, size, speed, health, direct_of_plane, coor_x, coor_y):
    plane = Plane(
        name=name,
        size=size,
        speed=speed,
        health=health,
        direct_of_plane=direct_of_plane,
        coor_x=coor_x,
        coor_y=coor_y,
    )
    db.session.add(plane)
    db.session.commit()
    return plane


def get_plane(plane_id):
    plane = Plane.query.filter_by(id=plane_id).first()
    return plane


def update_direction(plane_id, direct_of_plane):
    p = update(Plane).where(id == plane_id).values(direct_of_plane=direct_of_plane)
    return p
