from behave import given, then, when
from flask import url_for

from app.underwater.daos.session_dao import session_dao
from app.underwater.daos.submarine_dao import submarine_dao
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.models.submarine import Submarine
from app.underwater.models.torpedo import Torpedo
from app.underwater.session import UnderGameSession

### BACKGROUND ###


@given(
    "there is a game of dimension '{h:d}'x'{w:d}' with '{username1}' and '{username2}'"
)
def step_impl(context, h, w, username1, username2):
    host = context.players[username1]
    visitor = context.players[username2]
    context.game = game_dao.create(host=host, visitor=visitor, height=h, width=w)
    context.session = session_dao.start_session_for(context.game)

    assert context.game.host is host
    assert context.game.visitor is visitor


### ROTATE AND MOVE ###


@given("the submarines are in the following state")
def step_impl(context):
    for row in context.table:
        player = context.players[row["username"]]
        option_id = context.options[row["submarine"]]
        x = int(row["x_position"])
        y = int(row["y_position"])
        d = int(row["direction"])
        sub = context.game.add_submarine(player, option_id, x, y, d)
        sub.health = int(row["health"])


@given("the board is in the following state")
def step_impl(context):
    compare_board(context)


@when(
    "the user '{username}' rotates the submarine with direction '{d:d}' and moves '{n:d}' positions"
)
def step_impl(context, username, d, n):
    player = context.players[username]
    payload = {
        "direction": d,
        "steps": n,
    }
    # print(context.game)
    context.page = context.client.post(
        url_for(
            "underwater.rotate_and_advance",
            session_id=context.session.id,
            player_id=player.id,
        ),
        data=payload,
    )

    assert context.page


@then("the board is in the following state")
def step_impl(context):
    compare_board(context)


### ROTATE AND ATTACK ###


@when("the user '{username}' rotates the submarine with direction '{d:d}' and attacks")
def step_impl(context, username, d):
    player = context.players[username]
    payload = {
        "direction": d,
    }
    context.page = context.client.post(
        url_for(
            "underwater.rotate_and_attack",
            session_id=context.session.id,
            player_id=player.id,
        ),
        data=payload,
    )
    assert context.page


@then("fail")
def step_impl(context):
    assert False


def compare_board(context):
    board = context.game.board.matrix
    for i in range(context.game.height):
        for j in range(context.game.width):
            if context.table[i][j] == "H":
                assert (
                    type(board[i][j]) is Submarine
                    and board[i][j].x_position == i
                    and board[i][j].y_position == j
                )
            elif context.table[i][j] == "T":
                assert type(board[i][j] is Submarine)
            elif context.table[i][j] == "*":
                assert type(board[i][j]) is Torpedo
            else:
                assert board[i][j] is None
