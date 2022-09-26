def check_dynamic_data(data, pos_x, pos_y, dir):
    return (
        data["data"]["dynamic_data"]["ships"][0]["pos_x"] == pos_x
        and data["data"]["dynamic_data"]["ships"][0]["pos_y"] == pos_y
        and data["data"]["dynamic_data"]["ships"][0]["direction"] == dir
    )
