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


def get_genre_and_corr(anime_id, user=None, anime_ids=None):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    genre_score = Guesser.get_max_genre_match(anime_id, user=user, anime_ids=anime_ids)
    corr_score = Guesser.get_max_corr_match(anime_id, user=user, anime_ids=anime_ids)
    return corr_score, genre_score


def get_recommendation_score(anime_id, factors, user=None, anime_ids=None, threshold=0):
    rating, members = get_rating_and_members(anime_id)
    approximate_score = rating * factors[0] + members * factors[1] + abs(3 * factors[2])
    if factors[3] > 0:
        approximate_score += factors[3] * 3.5

    if approximate_score > threshold:
        if not user:
            user = Guesser.get_user_object()
        if not anime_ids:
            anime_ids = Guesser.get_anime_ids()
            
        corr, genre = get_genre_and_corr(anime_id, user=user, anime_ids=anime_ids)
    
        precise_score = rating * factors[0] + members * factors[1] + corr * factors[2] + genre * factors[3]
        record = [precise_score, anime_id]
        return record
    else:
        print('Skip')
        return None


def get_recs(factors, user=None, anime_ids=None, progress_log=False):
    if not user:
        user = Guesser.get_user_object()
    if not anime_ids:
        anime_ids = Guesser.get_anime_ids()

    recommendations = []
    top_10_results = []
    top_threshold = 0
    for titles_done, anime_id in enumerate(anime_ids, start=1):
        record = get_recommendation_score(anime_id, factors, user=user, anime_ids=anime_ids, threshold=top_threshold)

        if record:
            recommendations.append(record)
            top_10_results.append(record)
            top_10_results.sort(reverse=True)
            if len(top_10_results) >= 10:
                top_threshold = recommendations[9][0]
                if len(top_10_results) > 10:
                    top_10_results = top_10_results[:-1:]
        if progress_log:
            print(f'{titles_done / len(anime_ids) * 100}% Done')

    recommendations.sort(reverse=True)
    return recommendations


if __name__ == '__main__':
    max_side_score = 0

    user_obj = Guesser.get_user_object()
    anime_ids_list = Guesser.get_anime_ids()
    user_factors = Guesser.get_user_factors(user=user_obj, progress_log=True)
    print(user_factors)
    recs = get_recs(user_factors, user=user_obj, anime_ids=anime_ids_list, progress_log=True)
    for i in range(10):
        print(recs[i])

    print(len(recs))

# estimated score = factor1*rating + factor2*members + max_of_other2 * 2/3
