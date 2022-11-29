from flask import url_for


@then("the visibility of '{username}' is the following")
def step_impl(context, username):
    player = context.players[username]
    visibility = context.session.get_visible_state(player)["visible_board"]
    i = 0
    for row in context.table:
        for j in range(len(row)):
            si = str(i)
            sj = str(j)
            if row[j] == "":
                assert si not in visibility or sj not in visibility[si]
            else:
                assert si in visibility and sj in visibility[si]
                assert row[j] == visibility[si][sj]
        i += 1


@when("the player '{username}' sends a radar pulse")
def step_impl(context, username):
    player = context.players[username]
    session = context.session
    headers = {"authorization": context.tokens[player.id]}
    context.page = context.client.post(
        url_for("underwater.send_radar_pulse", session_id=session.id), headers=headers
    )
