import json

from app.daos.airforce.plane_dao import add_plane, add_projectile
from app.models.airforce.plane import Plane


def init_db():
    f = open("./app/models/airforce/planes.json")
    data = json.load(f)
    for plane in data["planes"]:
        name = plane["name"]
        size = plane["size"]
        speed = plane["speed"]
        health = plane["health"]
        cant_projectile = plane["cant_projectile"]
        # try:
        print("id", Plane.query.filter_by(name=name).first())
        if Plane.query.filter_by(name=name).first() == None:
            add_plane(name, size, speed, health, cant_projectile)
            # except:
            None
    for projectile in data["projectile"]:
        speed = projectile["speed"]
        damage = projectile["damage"]
        plane = Plane.query.filter_by(name=projectile["plane"]).first().id
        try:
            add_projectile(speed=speed, damage=damage, plane_id=plane)
        except:
            None
