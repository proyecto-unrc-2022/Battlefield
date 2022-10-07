from app import db
from ..models.submarine import Submarine


class SubmarineDAO:
    def __init__(self, submarine):
        self.submarine = submarine

    @staticmethod
    def create_submarine(
        game_id,
        player_id,
        name,
        size,
        speed,
        visibility,
        radar_scope,
        health,
        torpedo_speed,
        torpedo_damage,
        x_position=None,
        y_position=None,
        direction=None,
    ):
        sub = Submarine(
            game_id=game_id,
            player_id=player_id,
            name=name,
            size=size,
            speed=speed,
            visibility=visibility,
            radar_scope=radar_scope,
            health=health,
            torpedo_speed=torpedo_speed,
            torpedo_damage=torpedo_damage,
        )
        if x_position:
            sub.x_position = x_position
        if y_position:
            sub.y_position = y_position
        if direction:
            sub.direction = direction
        db.session.add(sub)
        db.session.commit()
        return SubmarineDAO(sub)

    @staticmethod
    def create_all(submarines):
        submarines_dao = []
        for sub in submarines:
            submarines_dao.append(SubmarineDAO(sub))
        return submarines_dao

    def is_placed(self):
        return self.submarine.x_position

    def update_position(self, x_coord=None, y_coord=None, direction=None):
        if x_coord:
            self.submarine.x_position = x_coord
        if y_coord:
            self.submarine.y_position = y_coord
        if direction:
            self.submarine.direction = direction
        db.session.commit()

    def get(sub_id):
        sub = db.session.query(Submarine).where(Submarine.id == sub_id).one_or_none()
        if not sub:
            raise ValueError("no submarine found with id %s" % sub_id)
        return SubmarineDAO(sub)

    def get_game(self):
        return self.submarine.game  # esta bien que retorne el juego?
        # return UnderGameDao(self.submarine.game.id)

    def get_submarine(self):
        return self.submarine
