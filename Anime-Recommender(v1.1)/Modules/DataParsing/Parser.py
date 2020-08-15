def find_mean(line):
    sum_of_values = 0
    for value in line:
        sum_of_values += value
    mean = sum_of_values / len(line)
    return mean


def calculate_deviation(line, mean):
    result = []
    for value in line:
        deviation_score = value - mean
        result.append(deviation_score)
    return result


def square_all(line):
    result = []
    for value in line:
        square = value ** 2
        result.append(square)
    return result


def get_sum(line):
    sum_of_values = 0
    for value in line:
        sum_of_values += value
    return sum_of_values


def cross_product(line_1, line_2):
    if len(line_1) != len(line_2):
        print('ERROR: lines have different length')
        return
    result = []
    for i in range(len(line_1)):
        multiplication_value = line_1[i] * line_2[i]
        result.append(multiplication_value)
    return result


def get_ratings_from_names_for(anime_id):
    import csv
    import codecs

    ratings = []
    with codecs.open('ratings-names.csv', 'r', 'utf_8_sig') as ratings_file:
        reader = csv.reader(ratings_file)
        for line in reader:
            if line[0] == anime_id:
                ratings.append(line)
    return ratings


def get_ratings_from_ids_for(anime_id):
    import csv
    import codecs

    ratings = []
    with codecs.open('ratings-ids.csv', 'r', 'utf_8_sig') as ratings_file:
        reader = csv.reader(ratings_file)
        for line in reader:
            if line[0] == anime_id:
                ratings.append(line)
    return ratings


def get_matching_ratings_names(anime_id_1, anime_id_2):
    result = []
    
    ratings_1 = get_ratings_from_names_for(anime_id_1)
    ratings_2 = get_ratings_from_names_for(anime_id_2)
    for rating_1 in ratings_1:
        user_name_1 = rating_1[1]
        for rating_2 in ratings_2:
            user_name_2 = rating_2[1]
            if user_name_1 == user_name_2:
                result.append(user_name_1)

    return result


def get_name_to_id_dict():
    import csv
    import codecs

    user_names_set = set()
    with codecs.open('ratings-names.csv', 'r', 'utf_8_sig') as ratings_file:
        reader = csv.reader(ratings_file)
        next(reader)
        for line in reader:
            user_names_set.add(line[1])

    name_to_id_dict = {}
    for i, name in enumerate(user_names_set, start=1):
        name_to_id_dict[name] = i

    return name_to_id_dict


def fill_ratings_with_ids_file():
    import csv
    import codecs

    name_to_id_dict = get_name_to_id_dict()

    with open('ratings-ids.csv', 'w', newline='', encoding='utf_8_sig') as ratings_ids_file:
        writer = csv.writer(ratings_ids_file, delimiter=',', quotechar='"')
        writer.writerow(['anime_id', 'user_id', 'rating'])

    with codecs.open('ratings-names.csv', 'r', 'utf_8_sig') as ratings_names_file:
        reader = csv.reader(ratings_names_file)
        next(reader)
        for i, line in enumerate(reader, start=1):
            if i % 1000 == 0:
                print(str(i) + ' lines done')

            anime_id = line[0]
            user_name = line[1]
            rating = line[2]

            user_id = name_to_id_dict[user_name]
            record = [anime_id, user_id, rating]
            with open('ratings-ids.csv', 'a', newline='', encoding='utf_8_sig') as ratings_ids_file:
                writer = csv.writer(ratings_ids_file, delimiter=',', quotechar='"')
                writer.writerow(record)
    print('Filling completed')


def reorganize_ratings():
    import csv
    import codecs

    anime_ids = []
    with codecs.open('anime-meta.csv', 'r', 'utf_8_sig') as anime_meta_file:
        reader = csv.reader(anime_meta_file)
        for line in reader:
            anime_ids.append(line[0])
    anime_ids = anime_ids[1::]

    for i, anime_id in enumerate(anime_ids, start=1):
        print(str(i / len(anime_ids) * 100) + '% Done')

        line = '[' + anime_id + '],'
        ratings = get_ratings_from_ids_for(anime_id)
        for rating in ratings:
            user_id = rating[1]
            anime_rating = rating[2]
            user_id = str(user_id)
            anime_rating = str(anime_rating)
            line += user_id + '-' + anime_rating + ','
        line = line[:-1:]
        line += '\n'
        with open('reorganized-ratings.txt', 'a') as reorganized_ratings_file:
            reorganized_ratings_file.write(line)


def get_ratings(anime_id):
    ratings = []
    with open('reorganized-ratings.txt', 'r') as ratings_file:
        lines = ratings_file.readlines()
        for line in lines:
            if line.startswith('[' + anime_id + ']'):
                line = line[:-1:]
                data = line.split(',')
                data = data[1::]
                for record in data:
                    user_id, rating = record.split('-')
                    ratings.append([user_id, rating])
                ratings.sort()
                return ratings
    return None


def get_matching_ratings(anime_id_1, anime_id_2):
    ratings_1 = get_ratings(anime_id_1)
    ratings_2 = get_ratings(anime_id_2)

    result_1 = []
    result_2 = []
    index_1 = 0
    index_2 = 0
    while index_1 < len(ratings_1) and index_2 < len(ratings_2):
        if int(ratings_1[index_1][0]) < int(ratings_2[index_2][0]):
            index_1 += 1
            continue
        if int(ratings_2[index_2][0]) < int(ratings_1[index_1][0]):
            index_2 += 1
            continue
        if int(ratings_1[index_1][0]) == int(ratings_2[index_2][0]):
            result_1.append(float(ratings_1[index_1][1]))
            result_2.append(float(ratings_2[index_2][1]))
            index_1 += 1
            index_2 += 1
            continue
    return result_1, result_2


def pearson_correlation(line_1, line_2):
    mean_1 = find_mean(line_1)
    mean_2 = find_mean(line_2)
    deviation_scores_1 = calculate_deviation(line_1, mean_1)
    deviation_scores_2 = calculate_deviation(line_2, mean_2)
    square_scores_1 = square_all(deviation_scores_1)
    square_scores_2 = square_all(deviation_scores_2)
    sum_of_squares_1 = get_sum(square_scores_1)
    sum_of_squares_2 = get_sum(square_scores_2)
    cross_products = cross_product(deviation_scores_1, deviation_scores_2)
    sum_of_products = get_sum(cross_products)

    if (sum_of_squares_1 ** 0.5) * (sum_of_squares_2 ** 0.5) != 0:
        correlation_coefficient = sum_of_products / ((sum_of_squares_1 ** 0.5) * (sum_of_squares_2 ** 0.5))
    else:
        correlation_coefficient = 0

    return correlation_coefficient


def get_correlation_score(anime_id, anime_id_2):
    first_ratings, second_ratings = get_matching_ratings(anime_id, anime_id_2)
    if len(first_ratings) < 7 or len(second_ratings) < 7:
        return 0
    correlation_score = pearson_correlation(first_ratings, second_ratings)
    return correlation_score


def get_meta(anime_id):
    import csv
    import codecs

    meta_info = {}
    with codecs.open('anime-meta.csv', 'r', 'utf_8_sig') as meta_file:
        reader = csv.reader(meta_file)
        next(reader)
        for line in reader:
            if line[0] == anime_id:
                meta_info['title'] = line[1]
                meta_info['rating'] = float(line[2])
                meta_info['members'] = int(line[3])
                meta_info['genres'] = line[4]

                return meta_info
    return None


def get_genre_similarity_score(anime_id_1, anime_id_2):
    genres_1 = get_meta(anime_id_1)['genres']
    genres_2 = get_meta(anime_id_2)['genres']
    genres_1 = genres_1.split(',')
    genres_2 = genres_2.split(',')

    matching_genres = 0
    for genre in genres_1:
        if genres_2.count(genre) != 0:
            matching_genres += 1

    similarity_score = matching_genres * 2 / (len(genres_1) + len(genres_2))
    return similarity_score


def get_max_members():
    import csv
    import codecs

    max_members = 0
    with codecs.open('anime-meta.csv', 'r', 'utf_8_sig') as meta_file:
        reader = csv.reader(meta_file)
        next(reader)
        for line in reader:
            members = int(line[3])
            max_members = max(max_members, members)
    return max_members


def get_recommendation_score(anime_id_1, anime_id_2):
    meta_2 = get_meta(anime_id_2)
    genre_score = get_genre_similarity_score(anime_id_1, anime_id_2)
    correlation_score = get_correlation_score(anime_id_1, anime_id_2)
    rating_2 = meta_2['rating']
    max_members = get_max_members()
    members_2 = meta_2['members']

    recommendation_score = (((correlation_score + 1) * 10)**2 + (genre_score * 100) + rating_2
                            + (members_2 * 3 / max_members)) / 513 * 100

    return recommendation_score
    
    
# TODO:
# def compute_data_base()


if __name__ == '__main__':
    score = get_recommendation_score('20', '1735')
    print(score)
