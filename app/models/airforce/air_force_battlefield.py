from app.models.airforce.air_force_flying_object import FlyingObject
from app.models.airforce.airforce_filters import get_player_plane
from app.models.airforce.plane import Projectile
from app.models.airforce.utils import rotate_plane


class Battlefield:
    flying_objects = []
    max_x = 20
    max_y = 10

    def __init__(self):
        self.flying_objects = []
        self.max_x = 20
        self.max_y = 10

    def add_new_flying_object(self, player, obj, x, y, course):
        if get_player_plane(self, player) != [] and obj.__class__.__name__ == "Plane":
            fly_obj = FlyingObject(player, obj, x, y, course)
            self.flying_objects.append(fly_obj)
        elif not self.position_inside_map(x, y):
            raise Exception("Invalid position")
        else:
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
            if fly_obj.flying_obj.__class__.__name__ == "Projectile":
                if fly_obj.update_position(course, self.max_x, self.max_y):
                    self.flying_objects.remove(fly_obj)
            elif fly_obj.flying_obj.__class__.__name__ == "Plane":
                if fly_obj.course != course:
                    rotate_plane(course, self, fly_obj.player)
                else:
                    for p in self.get_plane_parts(fly_obj):
                        p.update_position(course, self.max_x, self.max_y)
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
        self.destroy_plane(crashed)
        self.destroy_plane(crashing)

    def damage_plane(self, plane, damage):
        plane.flying_obj.health -= damage

    def destroy_plane(self, plane):
        if plane.flying_obj.health <= 0:
            plane_parts = self.get_plane_parts(plane)
            for p in plane_parts:
                self.flying_objects.remove(p)

    def get_plane_parts(self, plane):
        return list(
            filter(
                lambda p: p.flying_obj == plane.flying_obj and p.player == plane.player,
                self.flying_objects,
            )
        )

    def projectile_collision(self, projectile, fly_obj):
        if fly_obj.flying_obj.__class__.__name__ == "Plane":
            self.damage_plane(fly_obj, projectile.flying_obj.damage)
            self.destroy_plane(fly_obj)
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

    def get_status_player(self, player):
        from app.models.airforce.airforce_filters import get_player_plane

        plane = get_player_plane(self, player)[0]
        obj = list(
            filter(
                lambda p: p.x <= plane.x + 5
                and p.x >= plane.x - 5
                and p.y <= plane.y + 5
                and p.y >= plane.y - 5,
                self.flying_objects,
            )
        )
        l = {}
        i = 0
        for f in obj:
            l[i] = f.to_dict()
            i += 1
        return l
