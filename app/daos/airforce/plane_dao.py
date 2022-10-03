from sqlalchemy import update

from app import db
from app.models.airforce.plane import Plane, Projectile


def add_plane(name, size, speed, health, course, coor_x, coor_y):
    plane = Plane(
        name=name,
        size=size,
        speed=speed,
        health=health,
        course=course,
        coor_x=coor_x,
        coor_y=coor_y,
    )
    db.session.add(plane)
    db.session.commit()
    return plane


def get_plane(plane_id):
    plane = Plane.query.filter_by(id=plane_id).first()
    return plane


def update_course(plane_id, course):
    p = update(Plane).where(id == plane_id).values(course=course)
    return p


def add_projectile(speed, damage):
    projectile = Projectile(speed=speed, damage=damage)
    db.session.add(projectile)
    db.session.commit()
    return projectile


def get_projectile(projectile_id):
    projectile = Projectile.query.filter_by(id=projectile_id).first()
    return projectile
