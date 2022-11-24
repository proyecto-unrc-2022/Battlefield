from app.models.user import User
from battlefield import app
from tests.unit.underwater.test_generate_game import generate_game


def matrix_view_to_dict(matrix):
    result_dict = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j]:
                si = str(i)
                sj = str(j)
                if si in result_dict.keys():
                    result_dict[si].update({sj: matrix[i][j]})
                else:
                    result_dict.update({si: {sj: matrix[i][j]}})
    return result_dict


def test_visibility():
    with app.app_context():

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
        sub2 = game.submarines[1]

        expected_visitor_view = matrix_view_to_dict(
            [
                [None, None, "_", "_", "_", None],
                [None, None, "_", "FH0", "_", None],
                [None, None, "E*2", "FT0", "_", None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
            ]
        )
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view


def test_submarine_came_out():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    |    |    |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
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
                "x_coord": 0,
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
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        game.advance_object(sub1, 3)

        expected_visitor_view = matrix_view_to_dict(
            [
                [None, None, "_", "ET2", "EH2", None],
                [None, None, "_", "FH0", "_", None],
                [None, None, "_", "FT0", "_", None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
            ]
        )
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view


def test_torpedo_came_out():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    |    |    |    |
        #   1  |    |    |    | s2 |    |    |
        #   2  |    |    |    | s0 |    |    |
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
                "x_coord": 0,
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
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]

        game.attack(sub1)

        expected_visitor_view = matrix_view_to_dict(
            [
                [None, None, "E*2", "_", "_", None],
                [None, None, "_", "FH0", "_", None],
                [None, None, "_", "FT0", "_", None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
            ]
        )
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view


def test_advance_update_view():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    |    |    |    |
        #   1  |    |    |    | s2 | s0 | s0 |
        #   2  |    |    |    |    |    |    |
        #   3  |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |
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
                "x_coord": 0,
                "y_coord": 1,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 50,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 6,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub2 = game.submarines[1]

        game.advance_object(sub2, 1)

        expected_visitor_view = matrix_view_to_dict(
            [
                [None, "EH2", "_", "_", None, None],
                [None, "_", "FH6", "FT6", None, None],
                [None, "_", "_", "_", None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
            ]
        )
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view


def test_attack_update_view():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    |    |    |    |
        #   1  |    |    |    | s2 | s0 | s0 |
        #   2  |    |    |    |    |    |    |
        #   3  |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |
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
                "x_coord": 0,
                "y_coord": 1,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 50,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 6,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub2 = game.submarines[1]

        game.attack(sub2)

        expected_visitor_view = matrix_view_to_dict(
            [
                [None, None, "_", "_", "_", None],
                [None, None, "F*6", "FH6", "FT6", None],
                [None, None, "_", "_", "_", None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
            ]
        )
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view


def test_rotate_update_view():
    with app.app_context():

        #         0    1    2    3    4    5
        #      -------------------------------
        #   0  | s0 | s1 |    |    |    |    |
        #   1  |    |    |    | s2 | s0 | s0 |
        #   2  |    |    |    |    |    |    |
        #   3  |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |
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
                "x_coord": 0,
                "y_coord": 1,
                "direction": 2,
            },
            {
                "player": visitor,
                "chosen_id": 3,
                "health": 50,
                "x_coord": 1,
                "y_coord": 3,
                "direction": 6,
            },
        ]  # size = 4
        tor_list = []
        game = generate_game(6, 6, players, sub_list, tor_list)
        sub2 = game.submarines[1]

        game.rotate_object(sub2, 7)

        expected_visitor_view = matrix_view_to_dict(
            [
                [None, None, "_", "_", "_", None],
                [None, None, "_", "FH7", "_", None],
                [None, None, "_", "_", "FT7", None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, None, None, None, None],
            ]
        )
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
