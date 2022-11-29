from .airforce_filters import get_player_plane


# class Utils:
def position_inside_player_field(max_x, x, course, player, air_force_game):
    if air_force_game.player_a == player:
        if x > max_x / 2:
            return False
        if (x == (max_x / 2)) and course != 2:
            return False
    if air_force_game.player_b == player:
        if x <= max_x / 2:
            return False
        if (x == (max_x / 2) + 1) and course != 4:
            return False
    return True


def player_have_plane(battlefield, player):
    return get_player_plane(battlefield, player) != []


def projectile_avaible(player, battlefield):
    plane = get_player_plane(battlefield, player)[0]
    return plane.flying_obj.cant_projectile > 0


def discount_projectile(player, battlefield):
    plane = get_player_plane(battlefield, player)[0]
    plane.flying_obj.cant_projectile -= 1
