import db_communicator as db
import re


def to_searchable(line: str):
    line = line.lower()
    lines = line.split(',')
    for i in range(len(lines)):
        for symbol in lines[i]:
            if not symbol.isalpha() and not symbol.isdigit():
                lines[i] = lines[i].replace(symbol, '')
    lines = list(set(lines))
    lines.sort(key=len)
    return lines


def get_search_score(s: str, line: str):
    s = s.lower()
    parts = re.split(' |: |-|:', s)
    score = 0
    for part in parts:
        if line.find(part) != -1:
            score += 1
    return score


def find(search_line):
    titles = db.get_all_titles()
    search_titles = []
    for record in titles:
        anime_id, anime_titles = record
        new_record = [anime_id, to_searchable(anime_titles)]
        search_titles.append(new_record)

    search_results = []
    for anime in search_titles:
        anime_id = anime[0]
        titles = anime[1]
        best_title = titles[0]
        best_score = 0
        for title in titles:
            score = get_search_score(search_line, title)
            if score > best_score:
                best_score = score
                best_title = title
        result_record = [anime_id, best_score, best_title]
        search_results.append(result_record)
    
    search_results.sort(reverse=True, key=lambda x: (x[1], -len(x[2])))
    search_results = search_results[:10:]
    result_ids = []
    for search_result in search_results:
        result_ids.append(search_result[0])
    return result_ids


if __name__ == '__main__':
    print(find('Evangelion'))
