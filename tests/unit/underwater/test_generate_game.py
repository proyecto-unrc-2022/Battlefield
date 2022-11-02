from app.models.user import User
from app.underwater.board.under_board import UnderBoard
from app.underwater.models.under_game import UnderGame


def generate_game(h, w, players, sub_list, tor_list):
    game = UnderGame(players["host"], height=h, width=w)
    # game.board = UnderBoard(game.id, h, w)

    for sub in sub_list:
        if not game.host.submarine:
            submarine = generate_submarine(game.host, game, sub)
        else:
            game.visitor = players["visitor"]
            submarine = generate_submarine(game.visitor, game, sub)

        for tor in tor_list:
            if tor["player"] is sub["player"]:
                torpedo = (
                    submarine.create_torpedo()
                )  # in order to inherit the submarine's characteristics
                x = tor["x_coord"]
                y = tor["y_coord"]
                torpedo.set_position(
                    x, y, tor["direction"]
                )  # but I set the specified x,y and direction
                game.board.place(torpedo, (x, y))

    return game


def generate_submarine(player, game, sub):
    new_sub = game.add_submarine(
        player, sub["chosen_id"], sub["x_coord"], sub["y_coord"], sub["direction"]
    )
    new_sub.set_health(sub["health"])
    return new_sub


def test_generate_game_example():

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

    sub1 = game.get_submarines()[0]
    sub2 = game.get_submarines()[1]
    tor1 = game.get_torpedos()[0]
    tor2 = game.get_torpedos()[1]

    expected_board = [
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, tor2, None, None, None],
        [None, None, sub1, None, None, None, None, None, None, None, None, None],
        [None, None, None, sub1, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, sub2, None, None, None],
        [None, None, None, None, None, tor1, None, None, None, sub2, None, None],
    ]

    assert game.board.matrix == expected_board
