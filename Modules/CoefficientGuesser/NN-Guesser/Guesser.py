import sqlite3
import NN


def get_user():
    import json
    with open('user.json') as user_file:
        user = json.load(user_file)
    return user


def get_anime_ids():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute("""SELECT value
                    FROM system
                    WHERE variable_name='anime_ids'""")
    anime_ids_string = executor.fetchone()[0]
    connection.commit()
    connection.close()
    anime_ids = anime_ids_string.split(',')
    for i in range(len(anime_ids)):
        anime_ids[i] = int(anime_ids[i])
    return anime_ids


def get_max_members():
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT value
                    FROM system
                    WHERE variable_name='max_members'""")
    return int(executor.fetchone()[0])


def get_meta(anime_id):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT *
                    FROM anime_meta
                    WHERE anime_id={anime_id}""")
    data = list(executor.fetchone())
    meta = {'anime_id': data[0],
            'titles': data[1],
            'rating': data[2],
            'members': data[3],
            'genres': data[4]
            }
    connection.close()
    return meta


def get_genre_score(anime_id_1, anime_id_2, anime_ids=None):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                    FROM genre_scores
                    WHERE anime_id={anime_id_1}""")
    scores = executor.fetchone()[0]
    connection.close()

    if not anime_ids:
        anime_ids = get_anime_ids()
    ind = anime_ids.index(anime_id_2)
    scores = scores.split(',')
    return float(scores[ind])


def get_genre_scores(anime_id_1, second_ids, anime_ids=None):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                    FROM genre_scores
                    WHERE anime_id={anime_id_1}""")
    scores = executor.fetchone()[0]
    connection.close()

    if not anime_ids:
        anime_ids = get_anime_ids()

    result = []
    scores = scores.split(',')
    for anime_id_2 in second_ids:
        ind = anime_ids.index(anime_id_2)
        result.append(float(scores[ind]))
    return result


def get_correlation_score(anime_id_1, anime_id_2, anime_ids=None):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                    FROM correlation_scores
                    WHERE anime_id={anime_id_1}""")
    scores = executor.fetchone()[0]
    connection.close()

    if not anime_ids:
        anime_ids = get_anime_ids()
    ind = anime_ids.index(anime_id_2)
    scores = scores.split(',')
    return float(scores[ind])


def get_correlation_scores(anime_id_1, second_ids, anime_ids=None):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                    FROM correlation_scores
                    WHERE anime_id={anime_id_1}""")
    scores = executor.fetchone()[0]
    connection.close()

    if not anime_ids:
        anime_ids = get_anime_ids()

    result = []
    scores = scores.split(',')
    for anime_id_2 in second_ids:
        ind = anime_ids.index(anime_id_2)
        result.append(float(scores[ind]))
    return result


def get_genre_scores_for(anime_id):
    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""SELECT scores
                    FROM genre_scores
                    WHERE anime_id={anime_id}""")
    scores = executor.fetchone()[0]
    connection.close()

    scores = scores.split(',')
    for i in range(len(scores)):
        scores[i] = float(scores[i])
    return scores


def get_max_genre(anime_id, user=None, anime_ids=None):
    if not user:
        user = get_user()
    if not anime_ids:
        anime_ids = get_anime_ids()

    max_genre_score = -1
    max_genre_match = None

    watched_anime_ids = [int(watched_id) for watched_id in user]
    genre_scores = get_genre_scores(anime_id, watched_anime_ids, anime_ids=anime_ids)

    for i, watched_anime_id in enumerate(watched_anime_ids):
        if watched_anime_id == anime_id:
            continue
        genre_score = genre_scores[i]
        if genre_score > max_genre_score:
            max_genre_score = genre_score
            max_genre_match = int(watched_anime_id)

    best_match_user_rating = user[str(max_genre_match)]

    # print(f'Max genre score: {max_genre_score}')
    # print(f'Best genre match: {max_genre_match}')
    # print(f'Best genre match rating: {best_match_user_rating}')
    return max_genre_score, best_match_user_rating


def get_max_correlation(anime_id, user=None, anime_ids=None):
    if not user:
        user = get_user()
    if not anime_ids:
        anime_ids = get_anime_ids()

    max_correlation_score = -1
    max_correlation_match = None

    watched_anime_ids = [int(watched_id) for watched_id in user]
    correlation_scores = get_correlation_scores(anime_id, watched_anime_ids, anime_ids=anime_ids)

    for i, watched_anime_id in enumerate(watched_anime_ids):
        if watched_anime_id == anime_id:
            continue
        correlation_score = correlation_scores[i]
        if correlation_score > max_correlation_score:
            max_correlation_score = correlation_score
            max_correlation_match = int(watched_anime_id)

    best_match_user_rating = user[str(max_correlation_match)]

    # print(f'Max genre score: {max_genre_score}')
    # print(f'Best genre match: {max_genre_match}')
    # print(f'Best genre match rating: {best_match_user_rating}')
    return max_correlation_score, best_match_user_rating


def make_nn_input_for(anime_id):
    anime_ids = get_anime_ids()
    user = get_user()
    max_members = get_max_members()

    meta = get_meta(anime_id)
    rating = meta['rating']
    members = meta['members']

    max_genre_score, best_genre_match_user_rating = get_max_genre(anime_id, user=user, anime_ids=anime_ids)
    max_correlation_score, best_correlation_match_user_rating = \
        get_max_correlation(anime_id, user=user, anime_ids=anime_ids)

    rating_input = rating / 10 if rating else 0
    members_input = members / max_members
    genre_score_input = max_genre_score
    genre_rating_input = best_genre_match_user_rating / 10
    corr_score_input = (max_correlation_score + 1) / 2
    corr_rating_input = best_correlation_match_user_rating / 10

    return [
        rating_input,
        members_input,
        genre_score_input,
        genre_rating_input,
        corr_score_input,
        corr_rating_input,
    ]


def train_for_user():
    accuracy = 0.01

    # nn_specs = NN.Specification()
    # nn_specs.set_options(6, 1, 4, [5, 4, 3, 2], 0.1)
    # brain = NN.NeuralNetwork()
    # brain.set_specs(nn_specs)

    brain = NN.NeuralNetwork.deserialize('SerializedNN.json')

    current_error = 1e9
    last_n_results = []

    import time

    user = get_user()
    user_titles = list(user)

    brain.set_learning_rate(1 / len(user_titles))

    precomputed_inputs = {}
    for i, user_title in enumerate(user_titles, start=1):
        print(f'{i / len(user_titles) * 100}% of inputs computed')
        title_id = int(user_title)
        input_array = make_nn_input_for(title_id)
        precomputed_inputs[title_id] = input_array

    begin = time.process_time()

    ind_in_training_data = 0

    epochs = 1
    while current_error > accuracy and epochs < 100000:
        title = user_titles[ind_in_training_data]
        ind_in_training_data += 1
        if ind_in_training_data == len(user_titles):
            ind_in_training_data = 0
        input_array = precomputed_inputs[int(title)]
        target = [user[title] / 10]
        prediction = brain.predict(input_array)[0]
        last_n_results.append(abs(prediction - target[0]))
        if len(last_n_results) > len(user):
            last_n_results = last_n_results[1:]
        error_sum = sum(last_n_results)
        if len(last_n_results) >= len(user):
            current_error = error_sum / len(last_n_results)
        if epochs % 1000 == 0:
            print(f'{epochs} epochs, current error: {current_error * 10}')
        brain.train(input_array, target)
        epochs += 1
    end = time.process_time()

    print(f'Current error: {current_error * 10}')

    brain.serialize('SerializedNN.json')

    print('=======')
    for user_title in user_titles:
        input_array = make_nn_input_for(int(user_title))
        target = [user[user_title]]
        prediction = brain.predict(input_array)[0] * 10
        print(f'Title id: {user_title}, prediction: {round(prediction, 1)}, target: {target[0]}')
    print('=======')
    print(f'Finished in {end - begin}(s)')


def get_recommendations():
    anime_ids = get_anime_ids()
    brain = NN.NeuralNetwork.deserialize('SerializedNN.json')

    recs = []
    for i, anime_id in enumerate(anime_ids, start=1):
        print(f'{i / len(anime_ids) * 100}% Done')
        nn_input = make_nn_input_for(anime_id)
        score = brain.predict(nn_input)[0]
        record = [score, anime_id]
        recs.append(record)
        
    recs.sort(reverse=True)
    return recs


if __name__ == '__main__':
    recs = get_recommendations()
    for i in range(20):
        rec = recs[i]
        print(get_meta(rec[1])['titles'], rec[0] * 10)
