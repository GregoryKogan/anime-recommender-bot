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


# TODO:
# def get_ratings(anime_id):
# def get_matching_ratings(anime_id_1, anime_id_2)
# def get_correlation_score(anime_id, anime_id_2)
# def pearson_correlation(line_1, line_2)


if __name__ == '__main__':
    reorganize_ratings()
