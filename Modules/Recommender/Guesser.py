import GA
import Recommender


def build_training_data(user):
    watched_titles = list(user)
    for watched_title_ind in range(len(watched_titles)):
        watched_titles[watched_title_ind] = int(watched_titles[watched_title_ind])

    watched_titles_data = []
    for watched_title in watched_titles:
        _, _, genres, _, _, _ = Recommender.get_recommendation_data_for(watched_title)
        record = [watched_title, genres]
        watched_titles_data.append(record)

    training_data = []
    for watched_title in watched_titles:
        rating, members, genres, duration, episodes, age = Recommender.get_recommendation_data_for(watched_title)
        genre_score = 0
        for watched_title_data in watched_titles_data:
            if watched_title == watched_title_data[0]:
                continue
            else:
                current_genre_matching = Recommender.get_genre_score(genres, watched_title_data[1])
                second_rating = user[str(watched_title_data[0])] / 10
                current_genre_score = current_genre_matching * second_rating
                genre_score = max(genre_score, current_genre_score)
        training_test = {
            'Input': [rating, members, genre_score, duration, episodes, age],
            'Target': user[str(watched_title)]
        }
        training_data.append(training_test)
    return training_data


def get_user_factors(user):
    training_data = build_training_data(user)
    g = GA.Guesser(6, mutation_rate=1, population_size=250)
    epochs = 0
    while g.precision > 0.5 and epochs < 100:
        g.train(training_data)
        epochs += 1
    factors = g.test_formulas(training_data)[0]['formula'].factors
    return factors


if __name__ == '__main__':
    user_obj = Recommender.get_user()
    user_factors = get_user_factors(user_obj)
    print(user_factors)
