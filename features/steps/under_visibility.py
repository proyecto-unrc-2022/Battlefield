@then("the visibility of '{username}' is the following")
def step_impl(context, username):
    player = context.players[username]
    visibility = context.session.get_visible_state(player)["visible_board"]
    print(visibility)
    i = 0
    for row in context.table:
        for j in range(len(row)):
            if row[j] == "":
                assert i not in visibility or j not in visibility[i]
            else:
                assert row[j] == visibility[i][j]
        i += 1
