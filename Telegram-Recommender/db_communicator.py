import sqlite3
import json
from telebot.types import Message
import guesser


def get_all_titles():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("SELECT anime_id, titles FROM anime_meta")
    response = executor.fetchall()
    connection.close()
    return response


def get_meta_by_id(anime_id):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"SELECT * FROM anime_meta WHERE anime_id={anime_id}")
    response = executor.fetchone()
    connection.close()
    _, titles, genres, rating, members, episodes, duration, release_date, related = response
    meta = {
        'anime_id': anime_id,
        'titles': titles,
        'genres': genres,
        'rating': rating,
        'members': members,
        'episodes': episodes,
        'duration': duration,
        'release_date': release_date,
        'related': related
    }
    return meta


def get_user_name(message: Message):
    user_name = message.from_user.username
    if not user_name:
        user_name = message.from_user.first_name
    if not user_name:
        user_name = message.from_user.last_name
    if not user_name:
        user_name = 'Unknown user'
    return user_name


def get_user_data(user_id):
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute(f"SELECT user_name, chat_id FROM users_data WHERE user_id={user_id}")
    response = executor.fetchone()
    connection.close()
    return response


def check_user(message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    if not user_data:
        chat_id = message.chat.id
        user_name = get_user_name(message)
        connection = sqlite3.connect('Users.db')
        executor = connection.cursor()
        executor.execute(f"INSERT INTO users_data VALUES (:user_id, :user_name, :chat_id)",
                         {'user_id': user_id, 'user_name': user_name, 'chat_id': chat_id})
        connection.commit()
        connection.close()


def get_ratings_by(user_id):
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute(f"SELECT user_ratings FROM users_ratings_list WHERE user_id={user_id}")
    response = executor.fetchone()
    connection.close()
    if response:
        response = response[0]
    return response


def add_rating(user_id, anime_id, rating):
    user_ratings = get_ratings_by(user_id)
    if not user_ratings:
        user_ratings = {str(anime_id): rating}
        user_ratings = json.dumps(user_ratings)
        connection = sqlite3.connect('Users.db')
        executor = connection.cursor()
        executor.execute(f"INSERT INTO users_ratings_list VALUES (:user_id, :user_ratings)",
                         {'user_id': user_id, 'user_ratings': user_ratings})
        connection.commit()
        connection.close()
    else:
        user_ratings = json.loads(user_ratings)
        user_ratings[str(anime_id)] = rating
        user_ratings = json.dumps(user_ratings)
        connection = sqlite3.connect('Users.db')
        executor = connection.cursor()
        executor.execute(f"UPDATE users_ratings_list SET user_ratings='{user_ratings}' WHERE user_id={user_id}")
        connection.commit()
        connection.close()


def get_variable(variable_name):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"SELECT value FROM variables WHERE variable='{variable_name}'")
    response = executor.fetchone()[0]
    connection.close()
    return response


def get_anime_ids():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("SELECT value FROM variables WHERE variable='anime_ids'")
    response = executor.fetchone()[0].split(',')
    connection.close()
    result = [int(response[i]) for i in range(len(response))]
    return result


def get_recommendation_data_for(anime_id):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT rating, members, genres, duration, episodes, age
FROM recommendation_data WHERE anime_id={anime_id}""")
    response = executor.fetchone()
    connection.close()
    return response


def get_recommendation_data():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT * FROM recommendation_data""")
    response = executor.fetchall()
    connection.close()
    return response


def get_factors(user_id):
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute(f"SELECT factors FROM users_factors WHERE user_id={user_id}")
    response = executor.fetchone()
    connection.close()
    result = None
    if response:
        response = response[0]
        response = response.split(',')
        result = [float(response[factor_ind]) for factor_ind in range(len(response))]
    return result


def update_factors(user_id):
    user_ratings = json.loads(get_ratings_by(user_id))
    user_factors = guesser.get_user_factors(user_ratings, num_of_epochs=200)
    for factor_ind in range(len(user_factors)):
        user_factors[factor_ind] = str(user_factors[factor_ind])
    factors_string = ','.join(user_factors)
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    if get_factors(user_id):
        executor.execute(f"UPDATE users_factors SET factors='{factors_string}' WHERE user_id={user_id}")
    else:
        executor.execute(f"INSERT INTO users_factors VALUES (:user_id, :factors)",
                         {'user_id': user_id, 'factors': factors_string})
    connection.commit()
    connection.close()


if __name__ == '__main__':
    update_factors(544711957)
