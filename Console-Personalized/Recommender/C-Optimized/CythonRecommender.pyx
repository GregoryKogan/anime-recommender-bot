import sqlite3
import json
import concurrent.futures


def get_user():
    with open('user.json') as user_file:
        user_object = json.load(user_file)
        return user_object


cpdef list get_anime_ids():
    cdef object connection = sqlite3.connect('Recommender.db')
    cdef object executor = connection.cursor()
    executor.execute("""SELECT value FROM system WHERE variable_name='anime_ids'""")
    response = executor.fetchone()[0]
    connection.close()
    cdef list anime_ids_list = response.split(',')
    for i in range(len(anime_ids_list)):
        anime_ids_list[i] = int(anime_ids_list[i])
    return anime_ids_list


def get_anime_id_ind_dict(anime_ids_list):
    id_ind_dict = {}
    for i, anime_id in enumerate(anime_ids_list):
        id_ind_dict[int(anime_id)] = i
    return id_ind_dict


cpdef list get_input(int anime_id, dict anime_id_ind_dict, dict user):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT rating, members FROM anime_meta WHERE anime_id={anime_id}""")
    cdef float members
    cdef float rating
    rating_response, members = executor.fetchone()
    if not rating_response:
        rating = 0
    else:
        rating = rating_response
    executor.execute("""SELECT value FROM system WHERE variable_name='max_members'""")
    cdef float max_members
    max_members = float(executor.fetchone()[0])
    members = members / max_members * 10
    executor.execute(f"""SELECT scores FROM correlation_scores WHERE anime_id={anime_id}""")
    cdef list correlation_scores
    correlation_scores = executor.fetchone()[0].split(',')
    executor.execute(f"""SELECT scores FROM genre_scores WHERE anime_id={anime_id}""")
    cdef list genre_scores
    genre_scores = executor.fetchone()[0].split(',')
    cdef float max_corr_match_score = -1
    cdef int max_corr_match_id = 0
    cdef float max_genre_match_score = -1
    cdef int max_genre_match_id = 0
    cdef list watched_titles = list(user)
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
    cdef float corr_match_rating = executor.fetchone()[0]
    executor.execute(f"""SELECT rating FROM anime_meta WHERE anime_id={max_genre_match_id}""")
    cdef float genre_match_rating = executor.fetchone()[0]
    connection.close()
    cdef float corr_input = max_corr_match_score * corr_match_rating
    cdef float genre_input = max_genre_match_score * genre_match_rating
    cdef list result_input = [rating, members, corr_input, genre_input]
    cdef list function_res = [anime_id, result_input]
    return function_res


cpdef list get_recs(list anime_ids_list, dict anime_id_ind_dict, dict user, list user_factors, progress_log=False):
    cdef list recommendations = []
    cdef list watched_titles = list(user)
    cdef int titles_done = 0
    cdef list threads = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for anime_id in anime_ids_list:
            threads.append(executor.submit(get_input, anime_id, anime_id_ind_dict, user))

        for thread in concurrent.futures.as_completed(threads):
            titles_done += 1
            if progress_log:
                print(f'{titles_done / 100.0}% Done')
            response = list(thread.result())
            anime_id = response[0]
            formula_input = response[1]
            formula_output = 0
            for term_ind in range(len(formula_input)):
                formula_output += formula_input[term_ind] * user_factors[term_ind]
            record = [formula_output, anime_id]
            if str(anime_id) not in watched_titles:
                recommendations.append(record)
    recommendations.sort(reverse=True)
    return recommendations


cpdef get_recs_for_user_by_factors(dict user, list user_factors, progress_log=False):
    cdef list anime_ids = get_anime_ids()
    anime_id_ind_dictionary = get_anime_id_ind_dict(anime_ids)
    import time
    begin = time.perf_counter()
    cdef list recs = get_recs(anime_ids, anime_id_ind_dictionary, user, user_factors, progress_log=progress_log)
    end = time.perf_counter()

    if progress_log:
        for i in range(10):
            print(recs[i])
        print(f'Finished in {end - begin}(s)')

    
if __name__ == '__main__':
    factors = [1.0119084766654052, 0.2738593451543023, -0.19202096876447025, 0.16243546143742582]
    user_obj = get_user()
    get_recs_for_user_by_factors(user_obj, factors, progress_log=True)
