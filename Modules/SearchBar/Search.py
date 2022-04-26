def convert_to_searchable(line):
    line = line.lower()
    for symbol in line:
        if not (symbol.isalpha() or symbol.isdigit()):
            line = line.replace(symbol, '')
    return line


def convert_to_result_list(result_object):
    result_list = []
    max_similarity = 0
    for anime_name in result_object:
        similarity = result_object[anime_name]
        max_similarity = max(similarity, max_similarity)
        result_list.append([similarity, anime_name])
    result_list.sort(key=lambda x: x[0])

    most_similar = [
        result[1] for result in result_list if result[0] == max_similarity
    ]

    most_similar.sort(key=len)

    return most_similar


def find(line, titles):
    sub_lines = line.split(' ')
    for i in range(len(sub_lines)):
        sub_lines[i] = convert_to_searchable(sub_lines[i])

    results = {}
    for title in titles:
        for sub_line in sub_lines:
            if convert_to_searchable(title).find(sub_line) != -1:
                if title not in results:
                    results[title] = 0
                results[title] += 1

    results = convert_to_result_list(results)

    if len(results) > 0:
        return results

    return 'Not Found'


def get_titles():
    import csv
    import codecs
    anime_file = codecs.open('anime.csv', 'r', 'utf_8_sig')
    reader = csv.reader(anime_file)
    titles = [line[1] for line in reader]
    titles.pop(0)
    anime_file.close()
    return titles


def get_id_by_name(anime_name):
    import csv
    import codecs
    anime_file = codecs.open('anime.csv', 'r', 'utf_8_sig')
    reader = csv.reader(anime_file)

    for line in reader:
        if line[1] == anime_name:
            anime_file.close()
            return line[0]
    anime_file.close()
    return None


def testing():
    titles_list = get_titles()

    user_input = 'start'
    while user_input != 'exit':
        user_input = str(input('Find title: '))
        best_fit = find(user_input, titles_list.copy())

        if best_fit != 'Not Found':
            for i in range(min(3, len(best_fit))):
                print(f'{str(i + 1)}) {best_fit[i]}')
        else:
            print(best_fit)


def get_user_ratings():
    titles_list = get_titles()
    user_data = []

    user_input = 'start'
    while user_input != 'exit':
        user_input = str(input('Find title: '))

        if user_input == 'exit':
            continue

        best_fit = find(user_input, titles_list.copy())
        if best_fit == 'Not Found':
            print(best_fit)
            continue
        anime_name = best_fit[0]
        user_answer = str(input(f'Is it {anime_name}? - '))
        if user_answer == 'no':
            continue
        user_rating = float(input(f'Your rating for {anime_name}: '))

        record = [get_id_by_name(anime_name), user_rating]
        user_data.append(record)
    return user_data


def get_user_data():
    import csv
    import codecs
    user_file = codecs.open('user.csv', 'r', 'utf_8_sig')
    reader = csv.reader(user_file)

    next(reader)
    user = {line[0]: float(line[1]) for line in reader}
    user_file.close()
    return user


def collect_user_data():
    user = get_user_data()
    print('Your ratings: ')
    for anime in user:
        print(f'{anime} - {str(user[anime])}')

    new_ratings = get_user_ratings()
    print('New ratings collected')

    for new_rating in new_ratings:
        user[new_rating[0]] = new_rating[1]

    import csv
    import codecs
    user_file = codecs.open('user.csv', 'w', 'utf_8_sig')
    writer = csv.writer(user_file)
    writer.writerow(['anime_id', 'rating'])
    for anime in user:
        writer.writerow([anime, user[anime]])
    user_file.close()

    user = get_user_data()
    print('Your ratings: ')
    for anime in user:
        print(f'{anime} - {str(user[anime])}')


if __name__ == '__main__':
    collect_user_data()
