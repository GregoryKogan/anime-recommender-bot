def get_list_from_csv(file_name):
    import codecs
    import csv
    with codecs.open(file_name, 'r', 'utf_8_sig') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data


def get_line(file_name, line_index):
    import csv
    import codecs
    import itertools as it
    with codecs.open(file_name, 'r', 'utf_8_sig') as file:
        reader = csv.reader(file)
        result = next(it.islice(reader, line_index, line_index + 1))
    return result


def get_anime_ids():
    import csv
    import codecs

    anime_ids = []
    with codecs.open('anime-meta.csv', 'r', 'utf_8_sig') as anime_meta_file:
        reader = csv.reader(anime_meta_file)
        for line in reader:
            anime_ids.append(line[0])
    anime_ids = anime_ids[1::]
    return anime_ids


def get_meta_line(index):
    global meta_file
    return meta_file[index]


def get_meta_by_id(anime_id):
    global anime_ids

    meta_info = {}
    anime_meta_line = get_meta_line(anime_ids.index(anime_id) + 1)

    meta_info['title'] = anime_meta_line[1]
    try:
        meta_info['rating'] = float(anime_meta_line[2])
    except ValueError:
        meta_info['rating'] = 0
    meta_info['members'] = int(anime_meta_line[3])
    meta_info['genres'] = anime_meta_line[4]

    return meta_info


def get_max_members():
    global anime_ids
    max_members = 0
    for anime_id in anime_ids:
        members = get_meta_by_id(anime_id)['members']
        max_members = max(max_members, members)
    return max_members


def get_genre_score(anime_id_1, anime_id_2):
    global anime_ids
    row_index = anime_ids.index(anime_id_1) + 1
    column_index = anime_ids.index(anime_id_2)
    row = get_line('genre_score_table.csv', row_index)
    score = row[column_index]
    score = float(score)
    return score


def get_user():
    user = {
        '1535': 9.0,
        '16498': 9.3,
        '2904': 10.0
    }

    return user


def get_nn_input(anime_id_1, anime_id_2):
    global max_members
    meta_1 = get_meta_by_id(anime_id_1)
    meta_2 = get_meta_by_id(anime_id_2)
    user = get_user()

    # correlation_score = (None + 1) / 2
    correlation_score = 42
    genre_score = get_genre_score(anime_id_1, anime_id_2)
    crowd_rating_1 = meta_1['rating'] / 10
    crowd_rating_2 = meta_2['rating'] / 10
    members_1 = meta_1['members'] / max_members
    members_2 = meta_2['members'] / max_members
    user_rating = user[anime_id_1] / 10

    input_array = [correlation_score, genre_score, crowd_rating_1, crowd_rating_2, members_1, members_2, user_rating]

    return input_array


if __name__ == '__main__':
    print('Preparing...')
    anime_ids = get_anime_ids()
    meta_file = get_list_from_csv('anime-meta.csv')
    max_members = get_max_members()
    print('Preparation done')

    import time
    begin = time.process_time()
    print(get_nn_input('1535', '16498'))
    end = time.process_time()
    print(f'Finished in {end - begin}(s)')
