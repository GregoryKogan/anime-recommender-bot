import concurrent.futures
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


def get_estimated_score(anime_id, factors, user=None, anime_ids=None):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    args = get_input_for(anime_id, user=user, anime_ids=anime_ids)
    result = 0
    for arg_ind in range(len(args)):
        result += args[arg_ind] * factors[arg_ind]
    record = [result, anime_id]
    return record


def get_recs(factors, user=None, anime_ids=None, progress_log=False):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    recommendations = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = []
        for anime_id in anime_ids:
            threads.append(executor.submit(get_estimated_score, anime_id, factors, user=user, anime_ids=anime_ids))

        for thread in concurrent.futures.as_completed(threads):
            record = thread.result()
            recommendations.append(record)
            if progress_log:
                print(f'{len(recommendations) / len(anime_ids) * 100}% Done')

    recommendations.sort(reverse=True)
    return recommendations


if __name__ == '__main__':
    user_obj = Guesser.get_user_object()
    anime_ids_list = Guesser.get_anime_ids()
    user_factors = Guesser.get_user_factors(user=user_obj, progress_log=True)
    recs = get_recs(user_factors, user=user_obj, anime_ids=anime_ids_list, progress_log=True)
    for i in range(10):
        print(recs[i])
