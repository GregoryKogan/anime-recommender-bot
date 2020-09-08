import json
import guesser
import db_communicator as db
from telebot.types import Message


def get_genre_score(genres_1: str, genres_2: str):
    if len(genres_1) != len(genres_2):
        print('ERROR: genre strings have different length!')
        return None
    matching_sum = 0
    total_genres = 0
    for symbol_index in range(len(genres_1)):
        if genres_1[symbol_index] == '1' or genres_2[symbol_index] == '1':
            total_genres += 1
            if genres_1[symbol_index] == genres_2[symbol_index] == '1':
                matching_sum += 1
    genre_score = matching_sum / total_genres
    return genre_score


def get_user_watched_genres(user):
    user_watched_genres = []
    watched_titles = list(user)
    for title_ind in range(len(watched_titles)):
        watched_titles[title_ind] = int(watched_titles[title_ind])
    for watched_title in watched_titles:
        _, _, watched_title_genres, _, _, _ = db.get_recommendation_data_for(watched_title)
        rating = user[str(watched_title)]
        record = [rating, watched_title_genres]
        user_watched_genres.append(record)
    return user_watched_genres


def get_genre_input(genres, user_watched_genres):
    genre_input = 0
    for watched_title in user_watched_genres:
        rating = watched_title[0] / 10
        watched_genres = watched_title[1]
        genre_score = get_genre_score(genres, watched_genres)
        current_genre_input = rating * genre_score
        genre_input = max(genre_input, current_genre_input)
    return genre_input


def get_recommendations(user, factors):
    recommendations = []
    user_watched_genres = get_user_watched_genres(user)
    full_recommendation_data = db.get_recommendation_data()
    for recommendation_data_record in full_recommendation_data:
        anime_id, rating, members, genres, duration, episodes, age = recommendation_data_record
        if str(anime_id) in list(user):
            continue
        genre_input = get_genre_input(genres, user_watched_genres)
        formula_input = [rating, members, genre_input, duration, episodes, age]
        recommendation_score = 0
        for parameter_index in range(6):
            recommendation_score += formula_input[parameter_index] * factors[parameter_index]
        record = [recommendation_score, anime_id]
        recommendations.append(record)
    recommendations.sort(reverse=True)
    return recommendations


def recommend(message: Message, bot=None):
    user_id = message.from_user.id
    factors = db.get_factors(user_id)
    user = json.loads(db.get_ratings_by(user_id))
    recommendations = get_recommendations(user, factors)

    message_text = "<b>Your recommendations:</b>\n"
    for rec_ind in range(10):
        anime_id = recommendations[rec_ind][1]
        title = db.get_meta_by_id(anime_id)['titles'].split(',')[0]
        message_text += f"\n{rec_ind + 1}) {title}"
    bot.send_message(message.chat.id, message_text)


if __name__ == '__main__':
    import time
    user_obj = {"2904": 9.0, "1735": 9.5}
    user_factors = guesser.get_user_factors(user_obj, num_of_epochs=200)
    print(f'Factors: {user_factors}')
    begin = time.perf_counter()
    recs = get_recommendations(user_obj, user_factors)
    end = time.perf_counter()
    for i in range(10):
        print(recs[i])
    print(end - begin)
