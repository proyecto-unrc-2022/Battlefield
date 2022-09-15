import json
class Game:
    def read_data(file_path):
        with open(file_path) as file:
            data = json.load(file)

        return data

