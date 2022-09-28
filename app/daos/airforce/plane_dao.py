from sqlalchemy import update

from app import db
from app.models.airforce.plane import Plane


def add_plane(name, size, speed, health):
    plane = Plane(
        name=name,
        size=size,
        speed=speed,
        health=health
    )
    db.session.add(plane)
    db.session.commit()
    return plane


def get_plane(plane_id):
    plane = Plane.query.filter_by(id=plane_id).first()
    return plane


"""def update_course(plane_id, course):
    p = update(Plane).where(id == plane_id).values(course=course)
    return p"""
