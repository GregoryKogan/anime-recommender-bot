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


def fill_ratings_with_ids_file():
    import csv
    import codecs

    user_names_set = set()
    with codecs.open('ratings-names.csv', 'r', 'utf_8_sig') as ratings_file:
        reader = csv.reader(ratings_file)
        for line in reader:
            user_names_set.add(line[1])
    print(len(user_names_set))
    for name in user_names_set:
        print(name)


if __name__ == '__main__':
    fill_ratings_with_ids_file()
