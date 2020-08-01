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


def get_ratings(anime_id):
    return 42


'''This function computes pearson correlation score for two given anime titles'''


def compute_anime_correlation(id_1, id_2):
    global rating_list, anime_list
    for anime in anime_list:
        if int(anime['anime_id']) == id_1:
            print('First Anime: ' + anime['name'] + ' (' + str(id_1) + ')')
        if int(anime['anime_id']) == id_2:
            print('Second Anime: ' + anime['name'] + ' (' + str(id_2) + ')')
    print('Getting ratings')
    first_ratings = get_ratings(id_1)
    second_ratings = get_ratings(id_2)
    first_ratings, second_ratings = get_matching_ratings(first_ratings, second_ratings)
    correlation_coefficient = pearson_correlation(first_ratings, second_ratings)
    print(correlation_coefficient)
    return correlation_coefficient


'''This function reorganizes 'rating.csv' file to more convenient format and writes it to 'ReorganizedDB.txt' file'''


def compress_ratings_file():
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
    for i in range(5):
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
    task = str(input('Task: '))
    if task == 'compute reorganized ratings':
        compress_ratings_file()
    elif task == 'compute final data base':
        print('Computing final data base...')
