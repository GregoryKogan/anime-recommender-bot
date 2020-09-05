import sqlite3
import GA


def get_user_object():
    import json
    with open('user.json') as user_file:
        user_obj = json.load(user_file)
    return user_obj


def get_meta(anime_id):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT *
                        FROM anime_meta
                        WHERE anime_id={anime_id}""")
    response = executor.fetchone()
    meta_data = {
        'anime_id': response[0],
        'titles': response[1],
        'rating': response[2],
        'members': response[3],
        'genres': response[4]
    }
    if not meta_data['rating']:
        meta_data['rating'] = 0
    connection.close()
    return meta_data


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


def get_max_members():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""SELECT value
                        FROM system
                        WHERE variable_name='max_members'""")
    response = executor.fetchone()
    connection.close()

    max_members = int(response[0])
    return max_members


def get_max_genre_match(anime_id, user=None, anime_ids=None):
    if not user:
        user = get_user_object()
    if not anime_ids:
        anime_ids = get_anime_ids()

    watched_titles = list(user)
    for i in range(len(watched_titles)):
        watched_titles[i] = int(watched_titles[i])
    if anime_id in watched_titles:
        watched_titles.remove(anime_id)

    watched_titles_indexes = []
    for watched_title in watched_titles:
        title_ind = anime_ids.index(watched_title)
        watched_titles_indexes.append(title_ind)

    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                        FROM genre_scores
                        WHERE anime_id={anime_id}""")
    response = executor.fetchone()
    connection.close()

    scores = response[0].split(',')

    matching_scores = []
    for watched_title_index in watched_titles_indexes:
        matching_scores.append(float(scores[watched_title_index]))

    max_match_score = max(matching_scores)
    best_match_ind = matching_scores.index(max_match_score)
    best_match_id = watched_titles[best_match_ind]
    
    best_match_meta = get_meta(best_match_id)
    best_match_rating = best_match_meta['rating']

    score = max_match_score * best_match_rating
    return score


def get_max_corr_match(anime_id, user=None, anime_ids=None):
    if not user:
        user = get_user_object()
    if not anime_ids:
        anime_ids = get_anime_ids()

    watched_titles = list(user)
    for i in range(len(watched_titles)):
        watched_titles[i] = int(watched_titles[i])
    if anime_id in watched_titles:
        watched_titles.remove(anime_id)

    watched_titles_indexes = []
    for watched_title in watched_titles:
        title_ind = anime_ids.index(watched_title)
        watched_titles_indexes.append(title_ind)

    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                        FROM correlation_scores
                        WHERE anime_id={anime_id}""")
    response = executor.fetchone()
    connection.close()

    scores = response[0].split(',')

    matching_scores = []
    for watched_title_index in watched_titles_indexes:
        matching_scores.append(float(scores[watched_title_index]))

    max_match_score = max(matching_scores)
    best_match_ind = matching_scores.index(max_match_score)
    best_match_id = watched_titles[best_match_ind]

    best_match_meta = get_meta(best_match_id)
    best_match_rating = best_match_meta['rating']

    score = max_match_score * best_match_rating
    return score


def get_training_data_from_user(user=None):
    if not user:
        user = get_user_object()
    anime_ids = get_anime_ids()
    max_members = get_max_members()

    training_data = []
    for str_anime_id in user:
        anime_id = int(str_anime_id)
        user_rating = user[str_anime_id]
        meta = get_meta(anime_id)
        members = meta['members'] / max_members
        crowd_rating = meta['rating']
        genre_score = get_max_genre_match(anime_id, user=user, anime_ids=anime_ids)
        corr_score = get_max_corr_match(anime_id, user=user, anime_ids=anime_ids)
        new_test = {
            'Input': [crowd_rating, members, corr_score, genre_score],
            'Target': user_rating
        }
        training_data.append(new_test)
    return training_data


def get_user_factors(user=None, progress_log=False):
    if not user:
        user = get_user_object()

    if progress_log: print('Getting training data...')
    train_data = get_training_data_from_user(user=get_user_object())
    if progress_log: print('Training data collected')

    g = GA.Guesser(4, mutation_rate=0.1, population_size=250)
    precision_memory = [0] * 15
    gen_counter = 0
    guessed_formula = None
    while g.precision != precision_memory[0] and gen_counter < 100:
        g.train(train_data)
        best = g.test_formulas(train_data)[0]
        precision_memory.append(g.precision)
        precision_memory = precision_memory[1::]
        gen_counter += 1
        if progress_log: print(f'Gen: {gen_counter}, precision: {g.precision}')
        guessed_formula = best['formula']
    return guessed_formula.factors


if __name__ == '__main__':
    user_obj = get_user_object()
    import time
    begin = time.process_time()
    user_factors = get_user_factors(user=user_obj)
    end = time.process_time()
    print(user_factors)
    print(f'Finished in {end - begin}(s)')
