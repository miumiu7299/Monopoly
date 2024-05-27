import pickle

class Globals:
    selected_characters = {}
    current_player = 1
    players = 1
    money = 10000

    @staticmethod
    def get_data():
        return {
            'selected_characters': Globals.selected_characters,
            'current_player': Globals.current_player,
            'players': Globals.players,
            'money': Globals.money
        }

    @staticmethod
    def save_to_file(filename):
        data = Globals.get_data()
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
