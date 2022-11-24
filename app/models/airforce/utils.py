import json

from app import db
from app.daos.airforce.plane_dao import add_plane, add_projectile
from app.daos.user_dao import add_user, get_user_by_username
from app.models.airforce.plane import Plane


def init_db_planes():
    f = open("./app/models/airforce/planes.json")
    data = json.load(f)
    db.create_all()
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


def init_db_users():
    f = open("./app/models/airforce/planes.json")
    data = json.load(f)
    for user in data["users"]:
        username = user["username"]
        password = user["password"]
        email = user["email"]
        if get_user_by_username(username) == None:
            add_user(username=username, password=password, email=email)
