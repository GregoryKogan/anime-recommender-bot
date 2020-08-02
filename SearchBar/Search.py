def are_symbols_equal(symbol_1, symbol_2):
    if symbol_1 == symbol_2:
        return 0
    return 1


def convert_to_searchable(line):
    line = line.lower()
    for symbol in line:
        if not symbol.isalpha():
            line = line.replace(symbol, '')
    return line


def levenstein_dist(line_1, line_2):
    current = []

    for i in range(len(line_2) + 1):
        current.append(i)

    for i in range(len(line_1) + 1):
        previous = current.copy()
        current[0] = i
        for j in range(len(line_2) + 1):
            a = previous[j] + 1
            b = current[j - 1] + 1
            c = previous[j - 1] + are_symbols_equal(line_1[i - 1], line_2[j - 1])
            current[j] = min(a, b, c)
    return current[len(line_2)]


def same_letters_count(line_1, line_2):
    score = 0
    for symbol in line_1:
        result = line_2.find(symbol)
        if result != -1:
            line_2 = line_2.replace(symbol, '', 1)
            score += 1
    return score


def find(line, titles):
    line = convert_to_searchable(line)

    results = []
    for title in titles:
        if convert_to_searchable(title).find(line) != -1:
            results.append(title)
    if len(results) > 0:
        return results

    ind = 0
    while ind < len(titles):
        same_letters = same_letters_count(line, convert_to_searchable(titles[ind]))
        if same_letters < (len(line) / 3 * 2):
            titles.pop(ind)
            ind -= 1
        ind += 1

    while len(titles) > 0:
        nearest = 'Not Found'
        best_dist = 1e9
        for title in titles:
            dist = levenstein_dist(line, convert_to_searchable(title))
            if dist < best_dist:
                best_dist = dist
                nearest = title
        results.append(nearest)
        if nearest != 'Not Found':
            titles.remove(nearest)
            
    return results


def testing():
    titles_file = open('Titles.txt', 'r')
    titles_data = titles_file.read()
    titles_list = titles_data.split('\n')
    titles_file.close()

    user_input = 'start'
    while user_input != 'exit':
        user_input = str(input('Find title: '))
        best_fit = find(user_input, titles_list.copy())
        print(best_fit)


if __name__ == '__main__':
    testing()
    