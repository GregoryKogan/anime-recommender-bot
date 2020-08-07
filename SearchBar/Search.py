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

    results_by_score = [[]] * max_similarity
    for result in result_list:
        similarity = result[0]
        results_by_score[similarity - 1].append(result[1])

    for i in range(len(results_by_score)):
        results_by_score[i].sort(key=len)

    flat_results = []
    for group in results_by_score:
        for result in group:
            flat_results.append(result)

    return flat_results


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
    titles = []
    for line in reader:
        titles.append(line[1])
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
                print(str(i + 1) + ') ' + best_fit[i])
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
        user_answer = str(input('Is it ' + anime_name + '? - '))
        if user_answer == 'no':
            continue
        user_rating = int(input('Your rating for ' + anime_name + ': '))
        
        record = [get_id_by_name(anime_name), user_rating]
        user_data.append(record)
    return user_data


if __name__ == '__main__':
    user = get_user_ratings()
    print('--------------------')
    for record in user:
        print(record[0] + ' - ' + str(record[1]))
    # sub_lines = 'code r2'.split(' ')
    # for i in range(len(sub_lines)):
    #     sub_lines[i] = convert_to_searchable(sub_lines[i])
    # print(sub_lines)

