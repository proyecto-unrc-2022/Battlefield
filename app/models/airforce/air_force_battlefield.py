class FlyingObject:
    player = None
    flying_obj = None
    x: int = -1
    y: int = -1
    course = -1  # course 1 north, 2 east, 3 south, 4 west

    def __init__(self, player, flying_obj, x, y, course):
        self.player = player
        self.flying_obj = flying_obj
        self.x = x
        self.y = y
        self.course = course

    def check_course(self, course):
        #        raise Exception(self.course)
        return abs(self.course - course) == 2

    def update_position(self, course):
        if self.check_course(course):
            raise ValueError("New course cant be 180 degrees deference")
        if course == 1:
            self.y = self.y + self.flying_obj.speed
        elif course == 2:
            self.x = self.x + self.flying_obj.speed
        elif course == 3:
            self.y = self.y - self.flying_obj.speed
        elif course == 4:
            self.x = self.x - self.flying_obj.speed

    def to_dict(self):
        return {
            "player": self.player,
            "flying_obj": self.flying_obj.id,
            "x": self.x,
            "y": self.y,
            "course": self.course,
        }


class Battlefield:
    flying_objects = []
    max_x = 20
    max_y = 10

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

    @classmethod
    def position_inside_player_field(self, x, y, course, player, air_force_game):
        if air_force_game.player_a == player:
            if x > self.max_x / 2:
                return False
            if (x == (self.max_x / 2)) and course != 2:
                return False
        if air_force_game.player_b == player:
            if x <= self.max_x / 2:
                return False
            if (x == (self.max_x / 2) + 1) and course != 4:
                return False

        return True

    def add_new_plane(self, player, obj, x, y, course, air_force_game):
        if not self.position_inside_map(x, y):
            raise Exception("Invalid position")

        if not self.position_inside_player_field(x, y, course, player, air_force_game):
            raise Exception("Plane position cant be inside enemy field")

        if self.player_have_plane(player):
            raise Exception("This player already have a plane")

        fly_obj = FlyingObject(player, obj, x, y, course)
        self.flying_objects.append(fly_obj)
        return fly_obj

    def player_have_plane(self, player):
        return self.get_player_plane(player) != []

    def get_player_plane(self, player):
        return list(
            filter(
                lambda x: x.player == player
                and x.flying_obj.__class__.__name__ == "Plane",
                self.flying_objects,
            )
        )

    def fligth(self, player, course):
        obj = self.get_player_plane(player)[0]
        self.update_plane_position(course, obj)
        return obj

    def add_new_projectile(self, player, obj, x, y, course):
        fly_obj = FlyingObject(player, obj, x, y, course)
        if course == 1:
            fly_obj.y = fly_obj.y + 1
        elif course == 2:
            fly_obj.x = fly_obj.x + 1
        elif course == 3:
            fly_obj.y = fly_obj.y - 1
        elif course == 4:
            fly_obj.x = fly_obj.x - 1
        self.flying_objects.append(fly_obj)
        return fly_obj

    def move_projectile(self, player, course):
        obj = list(
            filter(
                lambda x: x.player == player
                and x.flying_obj.__class__.__name__ == "Projectile",
                self.flying_objects,
            )
        )
        print(self.flying_objects)
        for n in range(len(obj)):
            print(obj[n].to_dict())
            if course == 2 or course == 4:
                tupl = self.collision_x_projectile(obj[n], course)
                if tupl != ():
                    self.flying_objects.remove(tupl[0])
                    self.flying_objects.remove(tupl[1])
                else:
                    obj[n].update_position(course)
                    if obj[n].x >= 20 or obj[n].x <= 0:
                        self.flying_objects.remove(obj[n])
            if course == 1 or course == 3:
                tupl = self.collision_y_projectile(obj[n], course)
                if tupl != ():
                    self.flying_objects.remove(tupl[0])
                    self.flying_objects.remove(tupl[1])
                else:
                    obj[n].update_position(course)
                    if obj[n].y >= 10 or obj[n].y <= 0:
                        self.flying_objects.remove(obj[n])

        print(self.flying_objects)

    def collision_x_projectile(self, fly_obj, course):
        position = fly_obj.x
        speed = fly_obj.flying_obj.speed if course == 2 else -fly_obj.flying_obj.speed
        if speed > 0:
            projectile_coll = list(
                filter(
                    lambda p: p.y == fly_obj.y
                    and p.x > position
                    and p.x <= position + speed,
                    self.flying_objects,
                )
            )
            if projectile_coll != []:
                min_distance = min(projectile_coll, key=lambda p: p.x)
                return (fly_obj, min_distance)
        else:
            projectile_coll = list(
                filter(
                    lambda p: p.y == fly_obj.y
                    and p.x < position
                    and p.x >= position + speed,
                    self.flying_objects,
                )
            )
            if projectile_coll != []:
                min_distance = min(projectile_coll, key=lambda p: p.x)
                return (fly_obj, min_distance)
        return ()

    def collision_y_projectile(self, fly_obj, course):
        position = fly_obj.y
        speed = fly_obj.flying_obj.speed if course == 1 else -fly_obj.flying_obj.speed
        if speed > 0:
            projectile_coll = list(
                filter(
                    lambda p: p.x == fly_obj.x
                    and p.y > position
                    and p.y <= position + speed,
                    self.flying_objects,
                )
            )
            if projectile_coll != []:
                min_distance = min(projectile_coll, key=lambda p: p.y)
                return (fly_obj, min_distance)
        else:
            projectile_coll = list(
                filter(
                    lambda p: p.x == fly_obj.x
                    and p.y < position
                    and p.y >= position + speed,
                    self.flying_objects,
                )
            )
            if projectile_coll != []:
                min_distance = min(projectile_coll, key=lambda p: p.y)
                return (fly_obj, min_distance)
        return ()

    def update_plane_position(self, course, fly_obj):
        if fly_obj.check_course(course):
            raise ValueError("New course cant be 180 degrees deference")
        fly_obj.course = course
        if course == 1:
            self.colision_y(fly_obj, course)
            new_y = fly_obj.y + fly_obj.flying_obj.speed
            fly_obj.y = new_y if new_y <= self.max_y else self.max_y
        elif course == 2:
            self.colision_x(fly_obj, course)
            new_x = fly_obj.x + fly_obj.flying_obj.speed
            fly_obj.x = new_x if new_x <= self.max_x else self.max_x
        elif course == 3:
            self.colision_y(fly_obj, course)
            new_y = fly_obj.y - fly_obj.flying_obj.speed
            fly_obj.y = new_y if new_y >= 0 else 0
        elif course == 4:
            self.colision_x(fly_obj, course)
            new_x = fly_obj.x - fly_obj.flying_obj.speed
            fly_obj.x = new_x if new_x >= 0 else 0

    def colision_x(self, fly_obj, course):
        position = fly_obj.x
        speed = fly_obj.flying_obj.speed if course == 1 else -fly_obj.flying_obj.speed

        colision_obj = list(
            filter(
                lambda x: x.x < position and x.x >= position + speed,
                self.flying_objects,
            )
        )
        if colision_obj != []:
            obj = min(colision_obj, key=lambda x: x.x + speed)
            # raise Exception(obj.to_dict())
            obj.flying_obj.health -= fly_obj.flying_obj.health
            fly_obj.flying_obj.health -= obj.flying_obj.health

    def colision_y(self, plane, course):
        position = plane.y
        speed = plane.flying_obj.speed if course == 2 else -plane.flying_obj.speed
        colision_obj = list(
            filter(
                lambda p: p.y < position and p.y >= position + speed,
                self.flying_objects,
            )
        )
        if colision_obj != []:
            obj = min(colision_obj, key=lambda x: x.x + speed)
            # raise Exception('A = ', obj.to_dict(), plane.to_dict())
            obj.flying_obj.health -= plane.flying_obj.health
            plane.flying_obj.health -= obj.flying_obj.health
