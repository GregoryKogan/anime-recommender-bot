import sqlite3


def get_all_anime_ids_from_anime_meta():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""SELECT anime_id FROM anime_meta""")
    response = executor.fetchall()
    connection.close()
    anime_ids = [str(response[i][0]) for i in range(len(response))]
    anime_ids_string = ','.join(anime_ids)
    print(anime_ids_string)
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute('INSERT INTO variables VALUES (:variable, :value)',
                     {'variable': 'anime_ids', 'value': anime_ids_string})
    connection.commit()
    connection.close()


def get_anime_ids():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("SELECT value FROM variables WHERE variable='anime_ids'")
    response = executor.fetchone()[0].split(',')
    connection.close()
    result = [int(response[i]) for i in range(len(response))]
    return result


def get_property(property_name, anime_id):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"SELECT {property_name} FROM anime_meta WHERE anime_id={anime_id}")
    response = executor.fetchone()[0]
    connection.close()
    return response


def get_variable(variable_name):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"SELECT value FROM variables WHERE variable='{variable_name}'")
    response = executor.fetchone()[0]
    connection.close()
    return response


def get_all_genres():
    genres = set()
    anime_ids = get_anime_ids()
    for progress, anime_id in enumerate(anime_ids, start=1):
        print(f'{progress / len(anime_ids) * 100}% Done')
        current_genres = get_property('genres', anime_id).split(',')
        for genre in current_genres:
            if genre != '':
                genres.add(genre)
    genres = list(genres)
    genres.sort()
    return genres


def get_genre_coordinates(genres, anime_id):
    coordinates = ['0' for _ in range(len(genres))]
    anime_genres = get_property('genres', anime_id).split(',')
    for anime_genre in anime_genres:
        if anime_genre != '':
            genre_ind = genres.index(anime_genre)
            coordinates[genre_ind] = '1'
    coordinate_string = ''.join(coordinates)
    return coordinate_string


def get_recommendation_data(genres, anime_id):
    anime_rating = get_property('rating', anime_id)
    anime_members = get_property('members', anime_id)
    anime_episodes = get_property('episodes', anime_id)
    anime_duration = get_property('duration', anime_id)
    anime_date = get_property('release_date', anime_id)
    anime_genres = get_genre_coordinates(genres, anime_id)
    
    max_members = int(get_variable('max_members'))
    max_episodes = int(get_variable('max_episodes'))
    max_duration = int(get_variable('max_duration'))
    min_date = int(get_variable('min_release_date'))
    date_scale = 2021 - min_date

    anime_rating /= 10
    anime_members /= max_members
    anime_episodes /= max_episodes
    anime_duration /= max_duration
    anime_age = (2021 - anime_date) / date_scale
    
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""INSERT INTO recommendation_data VALUES 
    (:anime_id, :rating, :members, :genres, :duration, :episodes, :age)""",
                     {'anime_id': anime_id,
                      'rating': anime_rating,
                      'members': anime_members,
                      'genres': anime_genres,
                      'duration': anime_duration,
                      'episodes': anime_episodes,
                      'age': anime_age})

    connection.commit()
    connection.close()


def fill_recommendation_table():
    all_genres = get_all_genres()
    anime_ids = get_anime_ids()
    
    for progress, anime_id in enumerate(anime_ids, start=1):
        print(f'Filling {progress / len(anime_ids) * 100}% Done')
        get_recommendation_data(all_genres, anime_id)


if __name__ == '__main__':
    fill_recommendation_table()
