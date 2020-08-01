"""
This file works with 'rating.csv' and 'anime.csv' files in same directory
It produces new csv table with pearson correlation coefficient for any pair of anime titles
"""

"""This function calculates mean value for all elements in input list"""


def find_mean(line):
    sum_of_values = 0
    for value in line:
        sum_of_values += value
    mean = sum_of_values / len(line)
    return mean


"""This function calculates deviation from given mean and returns it as new list"""


def calculate_deviation(line, mean):
    result = []
    for value in line:
        deviation_score = value - mean
        result.append(deviation_score)
    return result


"""This function returns list with squares of elements in input list"""


def square_all(line):
    result = []
    for value in line:
        square = value ** 2
        result.append(square)
    return result


"""This function sum of all elements in given list"""


def get_sum(line):
    sum_of_values = 0
    for value in line:
        sum_of_values += value
    return sum_of_values


"""This function returns cross product of two lists. Result is another array with same length as both input lists"""


def cross_product(line_1, line_2):
    if len(line_1) != len(line_2):
        print('ERROR: lines have different length')
        return
    result = []
    for i in range(len(line_1)):
        multiplication_value = line_1[i] * line_2[i]
        result.append(multiplication_value)
    return result


def convert_to_list(ordered_dict):
    result = []
    for line in ordered_dict:
        result.append(line)
    return result


"""This function calculates Pearson correlation coefficient for to lists (lists need to have same length)"""


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

    '''debugging'''
    # print('mean 1: ', mean_1)
    # print('mean 2: ', mean_2)
    # print('deviation 1: ', deviation_scores_1)
    # print('deviation 2: ', deviation_scores_2)
    # print('squares 1: ', square_scores_1)
    # print('squares 2: ', square_scores_2)
    # print('SS 1: ', sum_of_squares_1)
    # print('SS 2: ', sum_of_squares_2)
    # print('Cross products: ', cross_products)
    # print('SP: ', sum_of_products)
    # print('Correlation coefficient: ', correlation_coefficient)

    return correlation_coefficient


'''This function finds all user ratings of given anime and returns them'''


def find_ratings(anime_id, rating_list, user_ids):
    ratings = []
    for review in rating_list:
        if int(review['anime_id']) == anime_id:
            user_id = int(review['user_id'])
            rating = int(review['rating'])
            if rating == -1:
                rating = None

            if rating is not None:
                record = [user_id, rating]
                ratings.append(record)
    return ratings


'''This function filters ratings for two titles. In the end there are only ratings from users that watched both'''


def get_matching_ratings(ratings_1, ratings_2):
    result_1 = []
    result_2 = []
    index_1 = 0
    index_2 = 0
    while index_1 < len(ratings_1) and index_2 < len(ratings_2):
        if ratings_1[index_1][0] < ratings_2[index_2][0]:
            index_1 += 1
            continue
        if ratings_2[index_2][0] < ratings_1[index_1][0]:
            index_2 += 1
            continue
        if ratings_1[index_1][0] == ratings_2[index_2][0]:
            result_1.append(ratings_1[index_1][1])
            result_2.append(ratings_2[index_2][1])
            index_1 += 1
            index_2 += 1
            continue
    return result_1, result_2


'''This function returns ratings for given anime title'''


def get_ratings(anime_id, ratings_list):
    ratings_string = None
    for line in ratings_list:
        if line.startswith('[' + str(anime_id) + ']'):
            ratings_string = line
            break
    reviews = ratings_string.split(',')
    reviews.pop(0)
    ratings = []
    for review in reviews:
        review = review[:-1]
        review = review[1:]
        values = review.split('-')
        user_id = int(values[0])
        rating = int(values[1])
        ratings.append([user_id, rating])
    return ratings


'''This function computes pearson correlation score for two given anime titles'''


def compute_anime_correlation(id_1, id_2, ratings_list):
    first_ratings = get_ratings(id_1, ratings_list)
    second_ratings = get_ratings(id_2, ratings_list)
    if len(first_ratings) == 0 or len(second_ratings) == 0:
        return 0
    first_ratings, second_ratings = get_matching_ratings(first_ratings, second_ratings)
    correlation_coefficient = pearson_correlation(first_ratings, second_ratings)
    return correlation_coefficient


'''This function reorganizes 'rating.csv' file to more convenient format and writes it to 'ReorganizedDB.txt' file'''


def compute_data_base():
    # importing libs for file management
    import csv
    import codecs

    # reading files
    print('Loading data')
    rating_file = codecs.open('rating.csv', 'r', 'utf_8_sig')
    anime_file = codecs.open('anime.csv', 'r', 'utf_8_sig')

    # making ordered dictionaries from files
    print('Preparing data')
    rating_ordered_dict = csv.DictReader(rating_file)
    anime_ordered_dict = csv.DictReader(anime_file)

    # converting ordered dictionaries to object lists
    rating_list = convert_to_list(rating_ordered_dict)
    anime_list = convert_to_list(anime_ordered_dict)

    print('Getting object ids')
    # getting list of all anime ids
    anime_ids = []
    for anime in anime_list:
        anime_ids.append(int(anime['anime_id']))

    # getting list of all user ids
    user_ids = []
    for rating in rating_list:
        if len(user_ids) == 0 or int(rating['user_id']) != user_ids[-1]:
            user_ids.append(int(rating['user_id']))

    print('Reorganizing data')
    import time
    anime_ratings = []
    for i in range(len(anime_ids)):
        begin_time = time.process_time()
        anime_id = anime_ids[i]
        ratings = find_ratings(anime_id, rating_list, user_ids)
        line = ''
        line += ('[' + str(anime_id) + ']')
        for review in ratings:
            user_id = review[0]
            rating = review[1]
            line += (',(' + str(user_id) + '-' + str(rating) + ')')
        line += '\n'
        anime_ratings.append(line)
        end_time = time.process_time()
        done_percent = (i + 1) / len(anime_ids) * 100
        print('Done ' + str(done_percent) + '% in ' + str(end_time - begin_time) + ' seconds')

    reorganized_db = open('ReorganizedDB.txt', 'w')
    reorganized_db.writelines(anime_ratings)

    # closing files
    rating_file.close()
    anime_file.close()
    reorganized_db.close()


if __name__ == '__main__':
    print("Print 'compute data base' or 'test'")
    task = str(input('Task: '))
    if task == 'compute data base':
        compute_data_base()
    elif task == 'test':
        print('Loading data')
        new_ratings_file = open('ReorganizedDB.txt', 'r')
        new_ratings = new_ratings_file.read()
        new_ratings_list = new_ratings.split('\n')
        import time
        user_input = 'start'
        print("Print 'exit' to stop or 'anime_id_1,anime_id_2' to get correlation coefficient")
        print('------------------')
        while str(user_input) != 'exit':
            user_input = str(input())
            if user_input != 'exit':
                values = user_input.split(',')
                anime_id_1 = values[0]
                anime_id_2 = values[1]
                begin_time = time.process_time()
                correlation_coefficient = compute_anime_correlation(anime_id_1, anime_id_2, new_ratings_list)
                end_time = time.process_time()
                print('Correlation coefficient is: ' + str(correlation_coefficient))
                print('Computation took: ' + str(end_time - begin_time) + ' seconds')
                print('------------------')
        new_ratings_file.close()
        print('------------------')

