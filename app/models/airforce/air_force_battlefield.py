from app.models.airforce.air_force_flying_object import FlyingObject
from app.models.airforce.airforce_filters import get_player_plane
from app.models.airforce.plane import Projectile


class Battlefield:
    flying_objects = []
    max_x = 20
    max_y = 10

    def __init__(self):
        self.flying_objects = []
        self.max_x = 20
        self.max_y = 10

    def add_new_flying_object(self, player, obj, x, y, course):
        if not self.position_inside_map(x, y):
            raise Exception("Invalid position")
        fly_obj = FlyingObject(player, obj, x, y, course)
        self.flying_objects.append(fly_obj)
        return fly_obj

    def position_inside_map(self, x, y):
        if x > self.max_x:
            return False
        if x < 1:
            return False
        if y > self.max_y:
            return False
        if y < 1:
            return False
        return True

    def move(self, fly_obj, course):
        self.check_colision(fly_obj, course)
        try:
            self.flying_objects.index(fly_obj)
            fly_obj.update_position(course, self.max_x, self.max_y)
        except:
            None

    def check_colision(self, fly_obj, course):
        if course == 1 or course == 3:
            self.colision_y(fly_obj, course)
        elif course == 2 or course == 4:
            self.colision_x(fly_obj, course)

    def colision_x(self, fly_obj, course):
        position = fly_obj.x
        if course == 2:
            speed = fly_obj.flying_obj.speed
            colision_obj = list(
                filter(
                    lambda object: object.x > position
                    and object.x <= position + speed
                    and object.y == fly_obj.y,
                    self.flying_objects,
                )
            )
        else:
            speed = -fly_obj.flying_obj.speed
            colision_obj = list(
                filter(
                    lambda object: object.x < position
                    and object.x >= position + speed
                    and object.y == fly_obj.y,
                    self.flying_objects,
                )
            )
        if colision_obj != []:
            obj = min(colision_obj, key=lambda obj: obj.x + speed)
            self.colision(fly_obj, obj)

    def colision_y(self, fly_obj, course):
        position = fly_obj.y
        if course == 1:
            speed = fly_obj.flying_obj.speed
            colision_obj = list(
                filter(
                    lambda p: p.y > position
                    and p.y <= position + speed
                    and p.x == fly_obj.x,
                    self.flying_objects,
                )
            )
        else:
            speed = -fly_obj.flying_obj.speed
            colision_obj = list(
                filter(
                    lambda p: p.y < position
                    and p.y >= position + speed
                    and p.x == fly_obj.x,
                    self.flying_objects,
                )
            )
        if colision_obj != []:
            obj = min(colision_obj, key=lambda obj: obj.y + speed)
            self.colision(fly_obj, obj)

    def colision(self, crashing, crashed):
        if crashed.flying_obj.__class__.__name__ == "Projectile":
            self.projectile_collision(crashed, crashing)
        elif crashing.flying_obj.__class__.__name__ == "Projectile":
            self.projectile_collision(crashing, crashed)
        else:
            self.plane_collision(crashing, crashed)

    def plane_collision(self, crashing, crashed):
        crashed_health = crashed.flying_obj.health
        crashed.flying_obj.health -= crashing.flying_obj.health
        crashing.flying_obj.health -= crashed_health
        self.flying_objects.remove(crashed) if (
            crashed.flying_obj.health <= 0
        ) else True
        self.flying_objects.remove(crashing) if (
            crashing.flying_obj.health <= 0
        ) else True

    def projectile_collision(self, projectile, fly_obj):
        if fly_obj.flying_obj.__class__.__name__ == "Plane":
            fly_obj.flying_obj.health -= projectile.flying_obj.damage
            self.flying_objects.remove(fly_obj) if (
                fly_obj.flying_obj.health <= 0
            ) else True
        else:
            self.flying_objects.remove(fly_obj)
        self.flying_objects.remove(projectile)

    def move_projectile(self, player):
        obj = list(
            filter(
                lambda x: x.player == player
                and x.flying_obj.__class__.__name__ == "Projectile",
                self.flying_objects,
            )
        )
        for n in obj:
            self.move(n, n.course)

    def check_course(self, course, player):
        obj = get_player_plane(self, int(player))
        if obj != []:
            print(course)
            if obj[0].check_invalid_course(int(course)):
                raise ValueError("New course cant be 180 degrees deference")

    def get_status(self):
        l = {}
        i = 0
        for f in self.flying_objects:
            l[i] = f.to_dict()
            i += 1
        return l
