from behave import given, then, when

from app.underwater.daos.submarine_dao import sub_dao
from app.underwater.daos.under_game_dao import game_dao
from app.underwater.models.submarine import Submarine
from app.underwater.models.torpedo import Torpedo


@given(
    "there is a game of dimension '{h:d}'x'{w:d}' with '{username1}' and '{username2}'"
)
def step_impl(context, h, w, username1, username2):
    host = context.players[username1]
    visitor = context.players[username2]
    context.game = game_dao.create(host.id, visitor.id, h, w)
    assert context.game.host is host
    assert context.game.visitor is visitor


@given("the submarines are in the following state")
def step_impl(context):
    for row in context.table:
        player = context.players[row["username"]]
        option_id = context.options[row["submarine"]]
        x = int(row["x_position"])
        y = int(row["y_position"])
        d = int(row["direction"])
        sub = context.game.add_submarine(player.id, option_id, x, y, d)
        sub.set_health(int(row["health"]))
        sub_dao.save(sub)


@given("the board is in the following state")
def step_impl(context):
    board = context.game.board.matrix
    for i in range(context.game.get_height()):
        for j in range(context.game.get_width()):
            if context.table[i][j] == "H":
                assert (
                    type(board[i][j]) is Submarine
                    and board[i][j].x_position == i
                    and board[i][j].y_position == j
                )
            elif context.table[i][j] == "T":
                print(type(board[i][j]))
                assert type(board[i][j] is Submarine)
            elif context.table[i][j] == "*":
                assert type(board[i][j]) is Torpedo


@when("the user 'player1' rotates the submarine with direction '7'")
def step_impl(context):
    pass


@then("the board is in the following state")
def step_impl(context):
    pass


@then("the submarines are in the following state")
def step_impl(context):
    pass
