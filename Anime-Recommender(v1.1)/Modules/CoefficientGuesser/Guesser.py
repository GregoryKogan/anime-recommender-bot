def get_user():
    import json
    with open('user.json') as user_file:
        user = json.load(user_file)
    return user


def make_nn_input_for(anime_id_1, anime_id_2):
    print('sec')


if __name__ == '__main__':
    import sqlite3
    make_nn_input_for('1535', '16498')
