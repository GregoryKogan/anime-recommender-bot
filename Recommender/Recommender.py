def get_user_data():
    # anime_id, rating
    data = [
        ['2904', 10],
        ['5114', 8],
        ['1535', 9],
        ['31240', 8.5],
        ['26055', 8.8]
    ]
    return data


def get_line(file_name, line_index):
    import csv
    import codecs
    file = codecs.open(file_name, 'r', 'utf_8_sig')
    reader = csv.reader(file)
    import itertools as it
    result = next(it.islice(reader, line_index, line_index + 1))
    file.close()
    return result


def get_anime_ratings():
    import csv
    import codecs
    file = codecs.open('crowd_ratings.csv', 'r', 'utf_8_sig')
    reader = csv.reader(file)
    anime_ratings = next(reader)
    file.close()
    return anime_ratings


def get_name_by_id(anime_id):
    import csv
    import codecs
    anime_file = codecs.open('anime.csv', 'r', 'utf_8_sig')
    anime_reader = csv.reader(anime_file)
    for line in anime_reader:
        if line[0] == anime_id:
            result = line[1]
            anime_file.close()
            return result
    anime_file.close()


def get_rating_by_id(anime_id):
    anime_ids = get_line('RecommenderDB.csv', 0)
    anime_ids.pop(0)
    line_index = anime_ids.index(anime_id) + 1
    info = get_line('anime.csv', line_index)
    if info[5] != '':
        return float(info[5])
    else:
        import requests
        import re
        a = requests.session()
        anime_name = get_name_by_id(anime_id)
        v = a.get('https://myanimelist.net/search/all?q=' + anime_name)
        try:
            k = re.findall(r'Scored \d.\d+', v.text)[0]
            k = re.findall(r'\d.\d+', k)[0]
            return float(k)
        except:
            return 5.00


def get_empty_recommendations_object(anime_ids):
    result = {}
    for anime_id in anime_ids:
        result[anime_id] = 0
    return result


def convert_to_recommendation_list(recommendation_object):
    result = []
    for anime_id in recommendation_object:
        score = recommendation_object[anime_id]
        recommendation = [score, anime_id]
        result.append(recommendation)
    result.sort()
    result.reverse()
    return result


def give_recommendations():
    user_data = get_user_data()

    anime_ids = get_line('RecommenderDB.csv', 0)
    anime_ids.pop(0)
    anime_ratings = get_anime_ratings()

    recommendations = get_empty_recommendations_object(anime_ids)

    for review in user_data:
        anime_id = review[0]
        user_rating = review[1]
        line_in_db = anime_ids.index(anime_id) + 1
        coefficients = get_line('RecommenderDB.csv', line_in_db)
        coefficients.pop(0)
        for i, coefficient in enumerate(coefficients):
            second_anime_id = anime_ids[i]
            crowd_rating = float(anime_ratings[anime_ids.index(second_anime_id)])
            score = float(coefficient) * user_rating * crowd_rating
            recommendations[second_anime_id] += score

    recommendation_list = convert_to_recommendation_list(recommendations)
    return recommendation_list


def write_ratings():
    anime_ids = get_line('RecommenderDB.csv', 0)
    anime_ids.pop(0)

    ratings = []
    for i in range(len(anime_ids)):
        print(str(round(i / len(anime_ids) * 100, 2)) + '%')
        rating = get_rating_by_id(anime_ids[i])
        ratings.append(rating)

    import csv
    import codecs
    file = codecs.open('crowd_ratings.csv', 'w', 'utf_8_sig')
    writer = csv.writer(file)
    writer.writerow(ratings)
    file.close()
    print('DONE')


if __name__ == '__main__':
    recs = give_recommendations()
    for i in range(10):
        print('You should watch: ' + get_name_by_id(recs[i][1]) + ', Score: ' + str(recs[i][0]))
