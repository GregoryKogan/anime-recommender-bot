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


def get_rating_and_members(anime_id):
    max_members = Guesser.get_max_members()
    meta = Guesser.get_meta(anime_id)
    members = meta['members'] / max_members
    crowd_rating = meta['rating']
    return crowd_rating, members


def get_genre_and_corr(anime_id, watched_titles, watched_titles_indexes, user=None, anime_ids=None):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    genre_score = Guesser.get_max_genre_match(anime_id,
                                              user=user, anime_ids=anime_ids,
                                              watched_titles=watched_titles,
                                              watched_titles_indexes=watched_titles_indexes)
    corr_score = Guesser.get_max_corr_match(anime_id,
                                            user=user, anime_ids=anime_ids,
                                            watched_titles=watched_titles,
                                            watched_titles_indexes=watched_titles_indexes)
    return corr_score, genre_score


def get_approximate_score(anime_id, factors):
    rating, members = get_rating_and_members(anime_id)
    approximate_score = rating * factors[0] + members * factors[1]
    return [approximate_score, anime_id]


def get_recommendation_score(anime_id, factors, approximate_score, watched_titles, watched_titles_indexes,
                             user=None, anime_ids=None):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()
            
    corr, genre = get_genre_and_corr(anime_id, watched_titles, watched_titles_indexes, user=user, anime_ids=anime_ids)
    
    precise_score = approximate_score + corr * factors[2] + genre * factors[3]
    return [precise_score, anime_id]


def get_recs(factors, user=None, anime_ids=None, progress_log=False):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    approximate_recs = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = []
        for anime_id in anime_ids:
            threads.append(executor.submit(get_approximate_score, anime_id, factors))
        for thread in concurrent.futures.as_completed(threads):
            record = thread.result()
            approximate_recs.append(record)
            if progress_log:
                print(f'Approximation {len(approximate_recs) / len(anime_ids) * 100}% Done')
    approximate_recs.sort(reverse=True)
    approximate_recs = approximate_recs[:500:]

    watched_titles = list(user)
    for title_ind in range(len(watched_titles)):
        watched_titles[title_ind] = int(watched_titles[title_ind])
    if anime_id in watched_titles:
        watched_titles.remove(anime_id)
    watched_titles_indexes = []
    for watched_title in watched_titles:
        title_ind = anime_ids.index(watched_title)
        watched_titles_indexes.append(title_ind)

    recommendations = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads = []
        for record in approximate_recs:
            current_approximate_score = record[0]
            anime_id = record[1]
            threads.append(executor.submit(get_recommendation_score, anime_id, factors, current_approximate_score,
                                           watched_titles, watched_titles_indexes,
                                           user=user, anime_ids=anime_ids))
        for thread in concurrent.futures.as_completed(threads):
            recommendation = thread.result()
            recommendations.append(recommendation)
            if progress_log:
                print(f'Recommendations {len(recommendations) / len(approximate_recs) * 100}% Done')
    recommendations.sort(reverse=True)
    return recommendations


if __name__ == '__main__':
    user_obj = Guesser.get_user_object()
    anime_ids_list = Guesser.get_anime_ids()
    user_factors = Guesser.get_user_factors(user=user_obj, progress_log=True)
    print(user_factors)
    recs = get_recs(user_factors, user=user_obj, anime_ids=anime_ids_list, progress_log=True)
    for i in range(10):
        print(recs[i])
