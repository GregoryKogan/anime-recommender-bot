import sqlite3
import Guesser


def get_input_for(anime_id, user=None, anime_ids=None):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    max_members = Guesser.get_max_members()
    meta = Guesser.get_meta(anime_id)
    members = meta['members'] / max_members
    crowd_rating = meta['rating']
    genre_score = Guesser.get_max_genre_match(anime_id, user=user, anime_ids=anime_ids)
    corr_score = Guesser.get_max_corr_match(anime_id, user=user, anime_ids=anime_ids)
    return [crowd_rating, members, corr_score, genre_score]


def get_recs(factors, user=None, anime_ids=None, progress_log=False):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    recommendations = []
    for ind, anime_id in enumerate(anime_ids, start=1):
        args = get_input_for(anime_id, user=user, anime_ids=anime_ids)
        result = 0
        for i in range(len(args)):
            result += args[i] * factors[i]
        record = [result, anime_id]
        if progress_log:
            print(f'{round(ind / len(anime_ids) * 100, 2)}% Done, record: {record}')
        recommendations.append(record)

    recommendations.sort(reverse=True)
    return recommendations


if __name__ == '__main__':
    user = Guesser.get_user_object()
    anime_ids = Guesser.get_anime_ids()
    user_factors = Guesser.get_user_factors(user=user, progress_log=True)
    recs = get_recs(user_factors, user=user, anime_ids=anime_ids, progress_log=True)
    for i in range(10):
        print(recs[i])
