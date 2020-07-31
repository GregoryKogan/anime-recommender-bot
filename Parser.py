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


def compute_anime_correlation(id_1, id_2):
    global rating_list, anime_list
    print(id_1, id_2)
    for anime in anime_list:
        if int(anime['anime_id']) == id_1 or int(anime['anime_id']) == id_2:
            print(anime['name'])


if __name__ == '__main__':
    # importing libs for file management
    import csv
    import codecs

    # reading files
    rating_file = codecs.open('rating.csv', 'r', 'utf_8_sig')
    anime_file = codecs.open('anime.csv', 'r', 'utf_8_sig')

    # making ordered dictionaries from files
    rating_ordered_dict = csv.DictReader(rating_file)
    anime_ordered_dict = csv.DictReader(anime_file)

    # converting ordered dictionaries to usual dictionaries
    rating_list = convert_to_list(rating_ordered_dict)
    anime_list = convert_to_list(anime_ordered_dict)

    # getting list of all anime ids
    anime_ids = []
    for anime in anime_list:
        anime_ids.append(anime['anime_id'])


    # compute_anime_correlation(32281, 28977)

    # closing files
    rating_file.close()
    anime_file.close()

'''
Main logic:
1). There is a function that i give to anime id's and it spits out correlation score for them
2). I have a csv table where cell with coordinats x and y contains correlation score for anime x and y
'''
