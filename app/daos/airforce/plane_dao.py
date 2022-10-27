from sqlalchemy import update

from app import db
from app.models.airforce.plane import Plane, Projectile, Machine_gun


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

def add_machine_gun(damage_1, damage_2, damage_3):
    machine_gun = Machine_gun(damage_1 = damage_1, damage_2 = damage_2, damage_3 = damage_3)
    db.session.add(machine_gun)
    db.session.commit()
    return machine_gun

def get_machine_gun(machine_gun_id):
    machine_gun = Machine_gun.query.filter_by(id=machine_gun_id).first()
    return machine_gun