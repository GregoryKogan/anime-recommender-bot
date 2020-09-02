import sqlite3
import json
from telebot.types import Message


def get_user_data(user_id):
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT *
                        FROM users_data
                        WHERE user_id={user_id}""")
    response = executor.fetchone()
    if response:
        response = list(response)
    connection.close()
    return response


def add_user(message: Message):
    user = message.from_user
    user_id = user.id
    user_name = 'Unknown'
    chat_id = message.chat.id
    if user.username:
        user_name = user.username
    elif user.first_name:
        user_name = user.first_name
    elif user.last_name:
        user_name = user.last_name

    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute("""INSERT INTO users_data VALUES
                        (:user_id, :user_name, :chat_id)""",
                     {'user_id': user_id, 'user_name': user_name, 'chat_id': chat_id})
    connection.commit()
    connection.close()


def get_all_titles():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""SELECT anime_id, titles FROM anime_meta""")
    response = list(executor.fetchall())
    connection.close()
    return response


def get_anime_meta(anime_id):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.execute(f"""SELECT *
FROM anime_meta
WHERE anime_id={anime_id}""")
    response = executor.fetchone()
    connection.close()
    if response:
        response = list(response)
    return response


def get_first_title_by_id(anime_id):
    meta = get_anime_meta(anime_id)
    titles = meta[1]
    titles = titles.split(',')
    first_title = titles[0]
    return first_title


def get_all_titles_by_id(anime_id):
    meta = get_anime_meta(anime_id)
    titles = meta[1]
    titles = titles.split(',')
    return titles


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_user_id_by_chat_id(chat_id):
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT user_id FROM users_data WHERE chat_id={chat_id}""")
    response = executor.fetchone()[0]
    connection.close()
    return response


def are_there_ratings_from(user_id):
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT * FROM users_ratings_list WHERE user_id={user_id}""")
    response = executor.fetchone()
    connection.close()
    if not response:
        return False
    else:
        return True


def get_user_ratings(user_id):
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT user_ratings FROM users_ratings_list WHERE user_id={user_id}""")
    response = executor.fetchone()
    connection.close()
    if response:
        result = json.loads(response[0])
        return result
    return response


def add_anime_rating(user_id, rating, anime_id):
    are_there_ratings = are_there_ratings_from(user_id)
    if are_there_ratings:
        user_ratings = get_user_ratings(user_id)
    else:
        user_ratings = {}
    user_ratings[str(anime_id)] = rating

    user_ratings = json.dumps(user_ratings)
    
    connection = sqlite3.connect('Users.db')
    executor = connection.cursor()
    if are_there_ratings:
        executor.execute(f"""UPDATE users_ratings_list 
SET user_ratings='{user_ratings}'
WHERE user_id={user_id}""")
    else:
        executor.execute(f"""INSERT INTO users_ratings_list VALUES (:user_id, :user_ratings)""",
                         {'user_id': user_id, 'user_ratings': user_ratings})
    connection.commit()
    connection.close()


def get_anime_ids():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""SELECT value
                        FROM system
                        WHERE variable_name='anime_ids'""")
    response = executor.fetchone()
    connection.close()

    anime_ids = response[0].split(',')
    for i in range(len(anime_ids)):
        anime_ids[i] = int(anime_ids[i])
    return anime_ids


if __name__ == '__main__':
    print(get_anime_ids())
