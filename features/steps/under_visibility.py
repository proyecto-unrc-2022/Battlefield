from flask import url_for


@then("the visibility of '{username}' is the following")
def step_impl(context, username):
    player = context.players[username]
    visibility = context.session.get_visible_state(player)["visible_board"]
    i = 0
    for row in context.table:
        for j in range(len(row)):
            if row[j] == "":
                assert i not in visibility or j not in visibility[i]
            else:
                assert i in visibility and j in visibility[i]
                assert row[j] == visibility[i][j]
        i += 1


@when("the player '{username}' sends a radar pulse")
def step_impl(context, username):
    player = context.players[username]
    session = context.session
    headers = {"authorization": context.tokens[player.id]}
    context.page = context.client.post(
        url_for("underwater.send_radar_pulse", session_id=session.id), headers=headers
    )


def dict_to_matrix(d, height, width):
    m = [[None] * width] * height
    for i in d:
        for j in d[i]:
            m[i][j] = d[i][j]
    return m
