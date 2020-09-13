import json
import guesser
import db_communicator as db
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


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

    user_id = message.from_user.id
    user_name, _ = db.get_user_data(user_id)
    message_text = f"Recommendation for <b>{user_name}</b>\n"
    anime_id = recommendations[0][1]
    title = db.get_first_title(anime_id)
    message_text += f"\n{title}"
    anime_poster = db.get_poster(anime_id)

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    rate_button = InlineKeyboardButton(text='Rate', callback_data='test')
    ban_button = InlineKeyboardButton(text='Ban', callback_data='test')
    next_button = InlineKeyboardButton(text='Next', callback_data='test')
    inline_keyboard.add(ban_button, rate_button,
                        next_button)

    if anime_poster and len(message_text) <= 1000:
        bot.send_photo(message.chat.id, anime_poster, caption=message_text, reply_markup=inline_keyboard)
    else:
        if anime_poster:
            bot.send_photo(message.chat.id, anime_poster)
            bot.send_message(message.chat.id, message_text, reply_markup=inline_keyboard)
        else:
            bot.send_message(message.chat.id, message_text, reply_markup=inline_keyboard)


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
