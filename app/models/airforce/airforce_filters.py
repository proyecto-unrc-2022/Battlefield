def get_player_plane(battlefield, player):
    return list(
        filter(
            lambda x: int(x.player) == int(player)
            and x.flying_obj.__class__.__name__ == "Plane",
            battlefield.flying_objects,
        )
    )
