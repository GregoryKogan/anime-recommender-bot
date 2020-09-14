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


def recommend(chat_id, recommendation_index, bot=None):
    user_id = db.get_user_id_by_chat_id(chat_id)
    factors = db.get_factors(user_id)
    user = json.loads(db.get_ratings_by(user_id))
    recommendations = get_recommendations(user, factors)

    user_name, _ = db.get_user_data(user_id)
    message_text = ""
    anime_id = recommendations[recommendation_index][1]
    recommendation_score = recommendations[recommendation_index][0]
    title = db.get_first_title(anime_id)
    anime_meta = db.get_meta_by_id(anime_id)
    alternative_titles = anime_meta['titles'].split(',')
    if len(alternative_titles) > 1:
        alternative_titles = alternative_titles[1::]
    else:
        alternative_titles = []
    genres = ', '.join(anime_meta['genres'].split(','))
    rating = anime_meta['rating']
    members = anime_meta['members']
    episodes = anime_meta['episodes']
    duration = anime_meta['duration']
    release_date = anime_meta['release_date']
    related_ids = list(map(int, anime_meta['related'].split(',')))
    message_text += f"<b>{title}</b>"
    if len(alternative_titles) > 0:
        message_text += '\n\nAlternative titles:'
        for alternative_title in alternative_titles:
            message_text += f'\n{alternative_title}'

    message_text += f'\n\nYear: <b>{release_date}</b>'
    message_text += f'\nRating: <b>{rating}</b>'
    message_text += f'\nViews: {members}'
    message_text += f'\n\nGenres:\n{genres}'
    message_text += f'\n\nEpisodes: {episodes}'
    message_text += f'\nEpisode duration: {duration} min(s)'

    real_related_ids = []
    for related_id in related_ids:
        if db.check_anime(related_id):
            real_related_ids.append(related_id)
    related_ids = real_related_ids
    if len(related_ids) > 0:
        message_text += '\n\nRelated to:'
        for related_id in related_ids:
            print(related_id)
            related_title = db.get_first_title(related_id)
            message_text += f'\n{related_title}'

    message_text += f"\n\nRecommendation for <b>{user_name}</b>"

    anime_poster = db.get_poster(anime_id)

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    rate_button = InlineKeyboardButton(text='Rate', callback_data='test')
    ban_button = InlineKeyboardButton(text='Ban', callback_data='test')
    if recommendation_index + 1 < len(recommendations):
        next_button = InlineKeyboardButton(text='Next', callback_data=f'next-{recommendation_index + 1}')
    else:
        next_button = InlineKeyboardButton(text='Next', callback_data=f'next-{0}')
    inline_keyboard.add(ban_button, rate_button,
                        next_button)

    if anime_poster and len(message_text) <= 1020:
        bot.send_photo(chat_id, anime_poster, caption=message_text, reply_markup=inline_keyboard)
    else:
        if anime_poster:
            bot.send_photo(chat_id, anime_poster)
            bot.send_message(chat_id, message_text, reply_markup=inline_keyboard)
        else:
            bot.send_message(chat_id, message_text, reply_markup=inline_keyboard)


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
