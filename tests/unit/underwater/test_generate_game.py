import json

from app.models.user import User
from app.underwater.board.board_mask import BoardMask
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.game_state import GameState
from app.underwater.models.submarine import Submarine
from app.underwater.models.torpedo import Torpedo
from app.underwater.models.under_game import UnderGame
from battlefield import app


def generate_game(h, w, players, sub_list, tor_list):
    game = UnderGame(players["host"], height=h, width=w)

    for sub in sub_list:
        if not game.host.submarine:
            submarine = generate_submarine(game.host, game, sub)
        else:
            game.visitor = players["visitor"]
            submarine = generate_submarine(game.visitor, game, sub)
            game.state = GameState.ONGOING

        for tor in tor_list:
            if tor["player"] is sub["player"]:
                torpedo = Torpedo(
                    game,
                    submarine.player,
                    speed=submarine.torpedo_speed,
                    damage=submarine.torpedo_damage,
                    x_position=tor["x_coord"],
                    y_position=tor["y_coord"],
                    direction=tor["direction"],
                )
                game.board.place_object(torpedo)

    return game


def generate_submarine(player, game, sub):
    with open("app/underwater/options.json") as f:
        options = json.load(f)
    new_sub = Submarine(
        game,
        player,
        options[str(sub["chosen_id"])],
        sub["x_coord"],
        sub["y_coord"],
        sub["direction"],
    )
    new_sub.health = sub["health"]
    new_sub.x_position = sub["x_coord"]
    new_sub.y_position = sub["y_coord"]
    new_sub.direction = sub["direction"]
    game.board.place_object(new_sub)
    mask = BoardMask(game, new_sub)
    return new_sub


def test_generate_game_example():
    with app.app_context():

        #         0    1    2    3    4    5    6    7    8    9   10   11
        #      -------------------------------------------------------------
        #   0  |    |    |    |    |    |    |    |    |    |    |    |    |
        #   1  |    |    |    |    |    |    |    |    | *2 |    |    |    |
        #   2  |    |    | s0 |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    | s1 |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    | s2 |    |    |    |
        #   5  |    |    |    |    |    | *1 |    |    |    | s0 |    |    |
        #      -------------------------------------------------------------

        host = User("player1", "player1", "player1@mail.com")
        visitor = User("player2", "player2", "player2@mail.com")
        players = {"host": host, "visitor": visitor}
        sub_list = [
            {
                "player": host,
                "chosen_id": 0,
                "health": 10,
                "x_coord": 3,
                "y_coord": 3,
                "direction": 3,
            },
            {
                "player": visitor,
                "chosen_id": 1,
                "health": 20,
                "x_coord": 4,
                "y_coord": 8,
                "direction": 7,
            },
        ]
        tor_list = [
            {"player": host, "x_coord": 5, "y_coord": 5, "direction": 3},
            {"player": visitor, "x_coord": 1, "y_coord": 8, "direction": 0},
        ]
        game = generate_game(6, 12, players, sub_list, tor_list)

        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        tor1 = game.torpedos[0]
        tor2 = game.torpedos[1]

        expected_board = [
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, tor2, None, None, None],
            [None, None, sub1, None, None, None, None, None, None, None, None, None],
            [None, None, None, sub1, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, sub2, None, None, None],
            [None, None, None, None, None, tor1, None, None, None, sub2, None, None],
        ]

        assert game.board.matrix == expected_board
