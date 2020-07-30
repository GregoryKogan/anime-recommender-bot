import sys


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


if __name__ == '__main__':
    line1 = [1, 2, 3, 4, 5]
    line2 = [2, 2, 4, 1, 9]
    coeff = pearson_correlation(line1, line2)
    print(coeff)

'''
Main logic:
1). There is a function that i give to anime id's and it spits out correlation score for them
2). I have a csv table where cell with coordinats x and y contains correlation score for anime x and y
'''
