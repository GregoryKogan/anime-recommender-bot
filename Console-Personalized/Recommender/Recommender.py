import sqlite3
import json
import concurrent.futures


def get_user():
    with open('user.json') as user_file:
        user_object = json.load(user_file)
        return user_object


def get_anime_ids():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""SELECT value FROM system WHERE variable_name='anime_ids'""")
    response = executor.fetchone()[0]
    connection.close()
    anime_ids_list = response.split(',')
    return anime_ids_list


def get_anime_id_ind_dict(anime_ids_list):
    id_ind_dict = {}
    for i, anime_id in enumerate(anime_ids_list):
        id_ind_dict[int(anime_id)] = i
    return id_ind_dict


def get_input(anime_id, anime_id_ind_dict, user):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT rating, members FROM anime_meta WHERE anime_id={anime_id}""")
    rating, members = executor.fetchone()
    if not rating:
        rating = 0
    executor.execute("""SELECT value FROM system WHERE variable_name='max_members'""")
    max_members = int(executor.fetchone()[0])
    members = members / max_members * 10
    executor.execute(f"""SELECT scores FROM correlation_scores WHERE anime_id={anime_id}""")
    correlation_scores = executor.fetchone()[0].split(',')
    executor.execute(f"""SELECT scores FROM genre_scores WHERE anime_id={anime_id}""")
    genre_scores = executor.fetchone()[0].split(',')
    max_corr_match_score = -1
    max_corr_match_id = 0
    max_genre_match_score = -1
    max_genre_match_id = 0
    watched_titles = list(user)
    for watched_title in watched_titles:
        watched_title = int(watched_title)
        if watched_title == anime_id:
            continue
        watched_title_ind = anime_id_ind_dict[watched_title]
        corr_score = float(correlation_scores[watched_title_ind])
        genre_score = float(genre_scores[watched_title_ind])
        if corr_score > max_corr_match_score:
            max_corr_match_score = corr_score
            max_corr_match_id = watched_title
        if genre_score > max_genre_match_score:
            max_genre_match_score = genre_score
            max_genre_match_id = watched_title
    executor.execute(f"""SELECT rating FROM anime_meta WHERE anime_id={max_corr_match_id}""")
    corr_match_rating = executor.fetchone()[0]
    executor.execute(f"""SELECT rating FROM anime_meta WHERE anime_id={max_genre_match_id}""")
    genre_match_rating = executor.fetchone()[0]
    connection.close()
    corr_input = max_corr_match_score * corr_match_rating
    genre_input = max_genre_match_score * genre_match_rating
    result_input = [rating, members, corr_input, genre_input]
    return anime_id, result_input


def get_recs(anime_ids_list, anime_id_ind_dict, user, factors):
    recommendations = []
    titles_done = 0
    threads = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for anime_id in anime_ids_list:
            threads.append(executor.submit(get_input, anime_id, anime_id_ind_dict, user))

        for thread in concurrent.futures.as_completed(threads):
            titles_done += 1
            print(f'{titles_done / 100}% Done')
            anime_id, formula_input = thread.result()
            formula_output = 0
            for term_ind in range(len(formula_input)):
                formula_output += formula_input[term_ind] * factors[term_ind]
            record = [formula_output, anime_id]
            recommendations.append(record)
    recommendations.sort(reverse=True)
    return recommendations


if __name__ == '__main__':
    user_factors = [1.0119084766654052, 0.2738593451543023, -0.19202096876447025, 0.16243546143742582]
    user_obj = get_user()
    anime_ids = get_anime_ids()
    anime_id_ind_dictionary = get_anime_id_ind_dict(anime_ids)
    import time
    begin = time.perf_counter()
    recs = get_recs(anime_ids, anime_id_ind_dictionary, user_obj, user_factors)
    end = time.perf_counter()
    for i in range(10):
        print(recs[i])
    print(f'Finished in {end - begin}(s)')
