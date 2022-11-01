from app.models.user import User
from tests.unit.underwater.test_generate_game import generate_game


def test_crash_submarine():

    #         0    1    2    3    4    5
    #      -------------------------------
    #   0  |    |    |    |    |    |    |
    #   1  |    |    |    | s2 |    |    |
    #   2  | s0 | s1 | *1 | s0 |    |    |
    #   3  |    |    |    | s0 |    |    |
    #   4  |    |    |    | s0 |    |    |
    #   5  |    |    |    |    |    |    |
    #      -------------------------------

    # GENERATE GAME
    host = User("player1", "player1", "player1@mail.com")
    visitor = User("player2", "player2", "player2@mail.com")
    players = {"host": host, "visitor": visitor}
    sub_list = [
        {
            "player": host,
            "chosen_id": 0,
            "health": 10,
            "x_coord": 2,
            "y_coord": 1,
            "direction": 2,
        },
        {
            "player": visitor,
            "chosen_id": 3,
            "health": 50,
            "x_coord": 1,
            "y_coord": 3,
            "direction": 0,
        },
    ]  # size = 4
    tor_list = [{"player": host, "x_coord": 2, "y_coord": 2, "direction": 2}]
    game = generate_game(6, 6, players, sub_list, tor_list)
    sub1 = game.get_submarines()[0]
    sub2 = game.get_submarines()[1]
    tor = game.get_torpedos()[0]

    # ACTION TO TEST
    game.advance_object(tor)

    # ASSERT
    expected_board = [
        [None, None, None, None, None, None],
        [None, None, None, sub2, None, None],
        [sub1, sub1, None, sub2, None, None],
        [None, None, None, sub2, None, None],
        [None, None, None, sub2, None, None],
        [None, None, None, None, None, None],
    ]

    assert game.board.matrix == expected_board
    assert sub2.health == 45
    assert len(game.get_submarines()) == 2
    assert len(game.get_torpedos()) == 0
    assert game.is_ongoing()


def test_destroy_submarine():

    #         0    1    2    3    4    5
    #      -------------------------------
    #   0  |    |    |    |    |    |    |
    #   1  |    |    |    | s2 |    |    |
    #   2  | s0 | s1 | *1 | s0 |    |    |
    #   3  |    |    |    | s0 |    |    |
    #   4  |    |    |    | s0 |    |    |
    #   5  |    |    |    |    |    |    |
    #      -------------------------------

    # GENERATE GAME
    host = User("player1", "player1", "player1@mail.com")
    visitor = User("player2", "player2", "player2@mail.com")
    players = {"host": host, "visitor": visitor}
    sub_list = [
        {
            "player": host,
            "chosen_id": 0,
            "health": 10,
            "x_coord": 2,
            "y_coord": 1,
            "direction": 2,
        },
        {
            "player": visitor,
            "chosen_id": 3,
            "health": 5,
            "x_coord": 1,
            "y_coord": 3,
            "direction": 0,
        },
    ]  # size = 4
    tor_list = [{"player": host, "x_coord": 2, "y_coord": 2, "direction": 2}]
    game = generate_game(6, 6, players, sub_list, tor_list)
    sub1 = game.get_submarines()[0]
    sub2 = game.get_submarines()[1]
    tor = game.get_torpedos()[0]

    # ACTION TO TEST
    game.advance_object(tor)

    # ASSERT
    expected_board = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [sub1, sub1, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
    ]

    assert game.board.matrix == expected_board
    assert len(game.get_submarines()) == 1
    assert len(game.get_torpedos()) == 0
    assert game.is_finished()


def test_crash_the_wall():

    #         0    1    2    3    4    5
    #      -------------------------------
    #   0  |    |    |    | *2 |    |    |
    #   1  |    |    |    | s2 |    |    |
    #   2  | s0 | s1 |    | s0 |    |    |
    #   3  |    |    |    | s0 |    |    |
    #   4  |    |    |    | s0 |    |    |
    #   5  |    |    |    |    |    |    |
    #      -------------------------------

    # GENERATE GAME
    host = User("player1", "player1", "player1@mail.com")
    visitor = User("player2", "player2", "player2@mail.com")
    players = {"host": host, "visitor": visitor}
    sub_list = [
        {
            "player": host,
            "chosen_id": 0,
            "health": 10,
            "x_coord": 2,
            "y_coord": 1,
            "direction": 2,
        },
        {
            "player": visitor,
            "chosen_id": 3,
            "health": 5,
            "x_coord": 1,
            "y_coord": 3,
            "direction": 0,
        },
    ]  # size = 4
    tor_list = [{"player": visitor, "x_coord": 0, "y_coord": 3, "direction": 0}]
    game = generate_game(6, 6, players, sub_list, tor_list)
    sub1 = game.get_submarines()[0]
    sub2 = game.get_submarines()[1]
    tor = game.get_torpedos()[0]

    # ACTION TO TEST
    game.advance_object(tor)

    # ASSERT
    expected_board = [
        [None, None, None, None, None, None],
        [None, None, None, sub2, None, None],
        [sub1, sub1, None, sub2, None, None],
        [None, None, None, sub2, None, None],
        [None, None, None, sub2, None, None],
        [None, None, None, None, None, None],
    ]

    assert game.board.matrix == expected_board
    assert len(game.get_submarines()) == 2
    assert len(game.get_torpedos()) == 0
    assert game.is_ongoing()
