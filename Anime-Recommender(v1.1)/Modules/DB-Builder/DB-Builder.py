import sqlite3


def fill_meta_table():
    import codecs
    import csv

    # connection = sqlite3.connect('Recommender.db')
    # executor = connection.cursor()
    #
    # executor.execute('''CREATE TABLE anime_meta
    #                 (anime_id integer, titles text, rating real, members integer, genres text)''')
    #
    # connection.commit()
    # connection.close()

    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    with codecs.open('anime-meta.csv', 'r', 'utf_8_sig') as meta_file:
        reader = csv.reader(meta_file)
        next(reader)
        for i, line in enumerate(reader, start=1):
            print(f'{i / 10000 * 100}% Done')

            anime_id = int(line[0])
            titles = line[1]
            try:
                rating = float(line[2])
            except ValueError:
                rating = None
            members = int(line[3])
            genres = line[4]

            executor.execute("""INSERT INTO anime_meta VALUES
            (:anime_id, :titles, :rating, :members, :genres)""",
                             {'anime_id': anime_id, 'titles': titles, 'rating': rating, 'members': members,
                              'genres': genres})
    connection.commit()
    connection.close()


def get_anime_ids():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""SELECT value
                    FROM system
                    WHERE variable_name='anime_ids'""")
    anime_ids_string = executor.fetchone()[0]
    connection.commit()
    connection.close()
    anime_ids = anime_ids_string.split(',')
    for i in range(len(anime_ids)):
        anime_ids[i] = int(anime_ids[i])
    return anime_ids


def fill_genre_score_table():
    import csv

    # connection = sqlite3.connect('Recommender.db')
    # executor = connection.cursor()
    #
    # executor.execute('''CREATE TABLE genre_scores
    #                 (anime_id integer, scores text)''')
    #
    # connection.commit()
    # connection.close()

    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()

    with open('genre_score_table.csv') as genre_file:
        reader = csv.reader(genre_file)
        anime_ids = next(reader)
        anime_ids[0] = anime_ids[0][3:]
        for row_num, line in enumerate(reader):
            print(f'{(row_num + 1) / 10000 * 100}% Done')

            anime_id = int(anime_ids[row_num])
            scores = ''
            for score in line:
                scores += ',' + score
            scores = scores[1:]

            executor.execute("""INSERT INTO genre_scores VALUES (:anime_id, :scores)""",
                             {'anime_id': anime_id, 'scores': scores})

    connection.commit()
    connection.close()


def fill_correlation_table():
    import csv

    # connection = sqlite3.connect('Recommender.db')
    # executor = connection.cursor()
    #
    # executor.execute('''CREATE TABLE correlation_scores
    #                 (anime_id integer, scores text)''')
    #
    # connection.commit()
    # connection.close()

    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()

    with open('correlation_score_table.csv') as correlation_file:
        reader = csv.reader(correlation_file)
        next(reader)
        for row_num, line in enumerate(reader):
            print(f'{(row_num + 1) / 10000 * 100}% Done')

            anime_id = int(line[0])
            scores = ''
            for i in range(1, len(line)):
                score = line[i]
                scores += ',' + score
            scores = scores[1:]

            executor.execute("""INSERT INTO correlation_scores VALUES (:anime_id, :scores)""",
                             {'anime_id': anime_id, 'scores': scores})

    connection.commit()
    connection.close()


def fill_system_table():
    import csv

    # connection = sqlite3.connect('Recommender.db')
    # executor = connection.cursor()
    #
    # executor.execute('''CREATE TABLE system
    #                 (variable_name text, value blob)''')
    #
    # connection.commit()
    # connection.close()

    with open('genre_score_table.csv') as genre_file:
        reader = csv.reader(genre_file)
        anime_ids = next(reader)
        anime_ids[0] = anime_ids[0][3:]
        anime_ids_string = ''
        for anime_id in anime_ids:
            anime_ids_string += ',' + anime_id
        anime_ids_string = anime_ids_string[1:]
        connection = sqlite3.connect('Recommender.db')
        executor = connection.cursor()
        executor.execute("""INSERT INTO system VALUES (:variable_name, :value)""",
                         {'variable_name': 'anime_ids', 'value': anime_ids_string})
        connection.commit()
        connection.close()


def get_genre_score(anime_id_1, anime_id_2):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                    FROM genre_scores
                    WHERE anime_id={anime_id_1}""")
    scores = executor.fetchone()[0]
    connection.close()

    anime_ids = get_anime_ids()
    ind = anime_ids.index(anime_id_2)
    scores = scores.split(',')
    return float(scores[ind])


if __name__ == '__main__':
    fill_correlation_table()

    # import time
    # begin = time.process_time()
    # score = get_genre_score(1535, 16498)
    # end = time.process_time()
    # print(score)
    # print(f'Finished in {end - begin}(s)')
