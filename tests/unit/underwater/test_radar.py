from app.models.user import User
from battlefield import app
from tests.unit.underwater.test_generate_game import generate_game
from tests.unit.underwater.test_player_visibility import matrix_view_to_dict

# [
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
# ]


def test_see_nothing():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  | s0 | s1 |    |    |    |    |    |    |    |    |    |    |    |    |    | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    |    | s2 | s0 | S0 |
        #      ----------------------------------------------------------------------------
        
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
                "chosen_id": 1,
                "health": 50,
                "x_coord": 9,
                "y_coord": 12,
                "direction": 6,
            },
        ]
        tor_list = []
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        
        # ACTION TO TEST
        game.send_radar_pulse(sub2)
        
        expected_visitor_view = matrix_view_to_dict(
            [
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_","FH6","FT6","FT6"],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                ["FT2","FH2",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view

def test_see_torpedo():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  | s0 | s1 |    |    |    |    |    |    |    |    |    |    |    |    |    | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    | *1 |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    |    | s2 | s0 | S0 |
        #      ----------------------------------------------------------------------------
        
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
                "chosen_id": 1,
                "health": 50,
                "x_coord": 9,
                "y_coord": 12,
                "direction": 6,
            },
        ]
        tor_list = [{"player": host, "x_coord": 3, "y_coord": 3, "direction": 2}]
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        
        # ACTION TO TEST
        game.send_radar_pulse(sub2)
        
        expected_visitor_view = matrix_view_to_dict(
            [
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rP", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_","FH6","FT6","FT6"],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                ["FT2","FH2",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_","F*2",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view

def test_see_submarine_and_i_wasnt_detected():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  | s0 | s1 |    |    |    |    |    |    |    |    |    |    |    |    |    | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    | *1 |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    | s2 | s0 | s0 |    |
        #      ----------------------------------------------------------------------------
        
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
                "chosen_id": 1,
                "health": 50,
                "x_coord": 9,
                "y_coord": 11,
                "direction": 6,
            },
        ]
        tor_list = [{"player": host, "x_coord": 3, "y_coord": 3, "direction": 2}]
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        
        # ACTION TO TEST
        game.send_radar_pulse(sub2)
        
        expected_visitor_view = matrix_view_to_dict(
            [
                [None, "rP", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rP", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_","FH6","FT6","FT6",  "_"],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                ["FT2","FH2",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_","F*2",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view

def test_see_submarine_but_i_was_dectected():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  | s0 | s1 |    |    |    |    |    |    |    |    |    |    |    |    |    | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    | *1 |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    | s2 | s0 | s0 |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #      ----------------------------------------------------------------------------
        
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
                "chosen_id": 1,
                "health": 10,
                "x_coord": 8,
                "y_coord": 8,
                "direction": 6,
            },
        ]
        tor_list = [{"player": host, "x_coord": 3, "y_coord": 3, "direction": 2}]
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        
        # ACTION TO TEST
        game.send_radar_pulse(sub2)
        
        # NOW BOTH SUBMARINES HAVE THE SAME RADAR-SCOPE
        expected_visitor_view = matrix_view_to_dict(
            [
                ["rP", "rP", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                ["rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                ["rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                ["rN", "rN", "rN", "rP", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                ["rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", "rN", "rN"],
                ["rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", "rN", "rN"],
                ["rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", "rN", "rN"],
                ["rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", "rN", "rN"],
                ["rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_","FH6","FT6","FT6",  "_",  "_", "rN", "rN"],
                ["rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", "rN", "rN"],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                ["FT2","FH2",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_","F*2",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, "rP", "rP", None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view

def test_see_submarine_but_i_was_dectected_2():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  | s0 | s1 |    |    |    |    |    |    |    |    |    |    |    |    |    | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    | *1 |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    |    | s2 | s0 |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #      ----------------------------------------------------------------------------
        
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
                "chosen_id": 0,
                "health": 10,
                "x_coord": 8,
                "y_coord": 9,
                "direction": 6,
            },
        ]
        tor_list = [{"player": host, "x_coord": 3, "y_coord": 3, "direction": 2}]
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        
        # ACTION TO TEST
        game.send_radar_pulse(sub2)
        
        # NOW BOTH SUBMARINES HAVE THE SAME RADAR-SCOPE
        expected_visitor_view = matrix_view_to_dict(
            [
                [None, "rP", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rP",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_","FH6","FT6",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                ["FT2","FH2",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_","F*2",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, "rP", None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view

def test_advance_and_clean_radar_cells():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  |    |    |    |    | *1 |    |    |    |    |    |    |    |    | s1 | s0 | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    | s2 | s0 | s0 |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #      ----------------------------------------------------------------------------
        
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
                "y_coord": 13,
                "direction": 6,
            },
            {
                "player": visitor,
                "chosen_id": 1,
                "health": 20,
                "x_coord": 6,
                "y_coord": 11,
                "direction": 6,
            },
        ]
        tor_list = [{"player": host, "x_coord": 0, "y_coord": 4, "direction": 6}]
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        
        # ACTION TO TEST
        game.send_radar_pulse(sub2)
        game.advance_object(sub2,3)
        game.rotate_object(sub2,0)
        game.advance_object(sub2,3)
        
        game.advance_object(sub1,3)
        
        # NOW BOTH SUBMARINES HAVE THE SAME RADAR-SCOPE
        expected_visitor_view = matrix_view_to_dict(
            [
                [None, "rN", "rN", "rN","E*6",  "_",  "_",  "_",  "_",  "_","EH6","ET6",  "_", "rP", "rP"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", "rN", "rN"],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_","FH0",  "_",  "_",  "_",  "_", None, None],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_","FT0",  "_",  "_",  "_",  "_", None, None],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_","FT0",  "_",  "_",  "_",  "_", None, None],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None],
                [None, "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_", None, None],
                [None, "rN", "rN", "rN", None, None, None, None, None, None, None, None, None, None, None],
                [None, "rN", "rN", "rN", None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                [None, None, None, None, None, "_" , "_" , "_" , "_" , "_" ,"FH6","FT6", "_" , "_" , "_" ],
                [None, None, None, None, None, "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" ],
                [None, None, None, None, None, "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" ],
                [None, None, None, None, None, "_" , "_" , "_" ,"EH0", "_" , "_" , "_" , "_" , "_" , "_" ],
                [None, None, None, None, None, "_" , "_" , "_" ,"ET0", "_" , "_" , "_" , "_" , "_" , "_" ],
                [None, None, None, None, None, "_" , "_" , "_" ,"ET0", "_" , "_" , "_" , "_" , "_" , "_" ],
                [None, None, None, None, None, None, None, None, None, None, None, "rP", "rP", "rP", None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view

def test_both_send_radar():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  |    |    |    |    | *1 |    |    |    |    |    |    |    |    | s1 | s0 | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    | s2 | s0 | s0 |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #      ----------------------------------------------------------------------------
        
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
                "y_coord": 13,
                "direction": 6,
            },
            {
                "player": visitor,
                "chosen_id": 1,
                "health": 20,
                "x_coord": 6,
                "y_coord": 11,
                "direction": 6,
            },
        ]
        tor_list = [{"player": host, "x_coord": 0, "y_coord": 4, "direction": 6}]
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        
        # ACTION TO TEST
        game.send_radar_pulse(sub2)
        
        game.advance_object(sub1,5)
        game.send_radar_pulse(sub1)
        game.advance_object(sub1,1)
        
        # NOW BOTH SUBMARINES HAVE THE SAME RADAR-SCOPE
        expected_visitor_view = matrix_view_to_dict(
            [
                [None, "rN", "rN", "rN", "rP", "rN", "rN", "rN", "rP", "rP", "rN", "rN", "rN", "rP", "rP"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_","FH6","FT6","FT6",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                ["rN", "rN", "_" , "_" ,"F*6", "_" , "_" ,"FH6","FT6", "_" , "_" , "_" , "_" , None, "rN"],
                ["rN", "rN", "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , None, "rN"],
                ["rN", "rN", "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , None, "rN"],
                ["rN", "rN", "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , None, "rN"],
                ["rN", "rN", "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , None, "rN"],
                ["rN", "rN", "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , "_" , None, "rN"],
                ["rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rP", "rP", "rP", "rN"],
                ["rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                ["rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view

def test_send_radar_two_times():
    with app.app_context():
        #         0    1    2    3    4    5    6    7    8   9    10   11   12   13   14
        #      ----------------------------------------------------------------------------
        #   0  |    |    |    |    |    |    |    |    |    |    |    |    |    |    | s1 | 
        #   1  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   2  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   3  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   4  |    |    |    |    |    |    |    |    |    | *1 |    |    |    |    |    |
        #   5  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   6  |    |    |    |    |    |    |    |    |    |    |    | s2 | s0 | s0 |    |
        #   7  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   8  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #   9  |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
        #      ----------------------------------------------------------------------------
        
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
                "y_coord": 14,
                "direction": 6,
            },
            {
                "player": visitor,
                "chosen_id": 1,
                "health": 20,
                "x_coord": 6,
                "y_coord": 11,
                "direction": 6,
            },
        ]
        tor_list = [{"player": host, "x_coord": 4, "y_coord": 9, "direction": 6}]
        game = generate_game(10, 15, players, sub_list, tor_list)
        sub1 = game.submarines[0]
        sub2 = game.submarines[1]
        tor1 = game.torpedos[0]
        
        # ACTIONS TO TEST
        game.send_radar_pulse(sub2)
        
        game.send_radar_pulse(sub1)
        game.advance_object(sub1,5)
        game.advance_object(sub1,5)
        game.advance_object(sub1,4)
        game.send_radar_pulse(sub1)
        
        game
        
        # NOW BOTH SUBMARINES HAVE THE SAME RADAR-SCOPE
        expected_visitor_view = matrix_view_to_dict(
            [
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rP"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_","E*6",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_","FH6","FT6","FT6",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
                [None, "rN", "rN", "rN", "rN", "rN", "rN",  "_",  "_",  "_",  "_",  "_",  "_",  "_",  "_"],
            ]
        )
        expected_host_view = matrix_view_to_dict(
            [
                ["FH6","FT6", "_" , "_" , "_" , "_" , "rN", "rN", "rN", None, None, None, None, None, None],
                [ "_" , "_" , "_" , "_" , "_" , "_" , "rN", "rN", "rN", None, None, None, None, None, None],
                [ "_" , "_" , "_" , "_" , "_" , "_" , "rN", "rN", "rN", None, None, None, None, None, None],
                [ "_" , "_" , "_" , "_" , "_" , "_" , "rN", "rN", "rN", None, None, None, None, None, None],
                [ "_" , "_" , "_" , "_" , "_" , "_" , "rN", "rN", "rN", None, None, None, None, None, None],
                [ "_" , "_" , "_" , "_" , "_" , "_" , "rN", "rN", "rN", None, None, None, None, None, None],
                [ "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", None, None, None, None, None, None],
                [ "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", None, None, None, None, None, None],
                [ "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", "rN", None, None, None, None, None, None],
                [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ]
        )
        
        assert sub2.under_board_mask.get_visible_board() == expected_visitor_view
        assert sub1.under_board_mask.get_visible_board() == expected_host_view
