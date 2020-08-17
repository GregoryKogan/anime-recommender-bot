from bs4 import BeautifulSoup
import requests


def get_anime_list():
    anime_list = []

    for i in range(200):
        print(str(((i + 1) / 200 * 100)) + '% Done')

        anime_top_html = \
            requests.get('https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(i * 50)).text
        anime_top = BeautifulSoup(anime_top_html, 'lxml')
        for anime_paragraph in anime_top.find_all('div', class_='detail'):
            anime_paragraph = anime_paragraph.find('div', class_='di-ib clearfix')
            info = anime_paragraph.find('a', class_='hoverinfo_trigger fl-l fs14 fw-b')
            anime_name = info.text
            anime_link = info['href']
            anime_id = anime_link.split('/')[4]
            anime_record = [anime_id, anime_name, anime_link]
            anime_list.append(anime_record)

    import csv
    import codecs
    anime_list_file = codecs.open('anime-list.csv', 'w', 'utf_8_sig')
    writer = csv.writer(anime_list_file)
    writer.writerow(['anime_id', 'name', 'link'])
    writer.writerows(anime_list)
    anime_list_file.close()


def get_meta_info(anime_link):
    anime_page_html = requests.get(anime_link).text
    anime_page = BeautifulSoup(anime_page_html, 'lxml')

    main_title = anime_page.find('span', itemprop="name")
    if main_title:
        main_title = main_title.contents[0]

    title_recs = []
    for title_div in anime_page.find_all('div', class_='spaceit_pad'):
        title_recs.append(title_div.text)
    title_recs = title_recs[0:2:1]
    all_titles = []
    if main_title:
        all_titles.append(main_title)
    for record in title_recs:
        data = record[1::]
        data = data[0:-3:]
        if data.startswith('English: '):
            data = data[9::]
        if data.startswith('Synonyms: '):
            data = data[10::]
        if data.startswith('Japanese: '):
            sub_titles = []
        else:
            sub_titles = data.split(', ')
        for title in sub_titles:
            all_titles.append(title)
    if len(all_titles) > 1:
        if all_titles[0] == all_titles[1]:
            all_titles = all_titles[1::]
    titles_string = ''
    for title in all_titles:
        titles_string += title + ','
    titles_string = titles_string[:-1:]

    anime_id = anime_link.split('/')[4]

    score_div = anime_page.find('div', class_='score-label')
    rating = score_div.text

    members_span = anime_page.find('span', class_='numbers members')
    members = members_span.strong.text
    members = members.replace(',', '')

    generes_string = ''
    for genere_span in anime_page.find_all('span', itemprop="genre"):
        generes_string += genere_span.text + ','
    generes_string = generes_string[:-1:]

    meta_info = [anime_id, titles_string, rating, members, generes_string]
    return meta_info


def get_last_filled_line():
    import csv
    import codecs

    with codecs.open('anime-meta.csv', 'r', 'utf_8_sig') as anime_meta_file:
        reader = csv.reader(anime_meta_file)
        total_lines = 0
        for line in reader:
            last_id = line[0]
            total_lines += 1

    anime_ids = []
    with codecs.open('anime-list.csv', 'r', 'utf_8_sig') as anime_list:
        reader = csv.reader(anime_list)
        next(reader)
        for line in reader:
            anime_ids.append(line[0])

    if total_lines > 1:
        ind = anime_ids.index(last_id) + 1
    else:
        ind = 0
    return ind


def fill_meta_file():
    import csv
    import codecs

    anime_links = []
    with codecs.open('anime-list.csv', 'r', 'utf_8_sig') as anime_list:
        reader = csv.reader(anime_list)
        next(reader)
        for line in reader:
            anime_links.append(line[2])

    with codecs.open('anime-meta.csv', 'r', 'utf_8_sig') as meta_file:
        reader = csv.reader(meta_file)
        total_lines = 0
        for _ in reader:
            total_lines += 1

    if total_lines == 0:
        with codecs.open('anime-meta.csv', 'w', 'utf_8_sig') as meta_file:
            writer = csv.writer(meta_file)
            writer.writerow(['anime_id', 'titles', 'rating', 'members', 'genres'])

    last_filled_line = get_last_filled_line()
    anime_links = anime_links[last_filled_line::]
    print('Starting from: ' + anime_links[0])
    for i, link in enumerate(anime_links):
        print(link)
        meta_info = get_meta_info(link)
        with open('anime-meta.csv', 'a', newline='', encoding='utf_8_sig') as meta_file:
            writer = csv.writer(meta_file, delimiter=',', quotechar='"')
            writer.writerow(meta_info)
        print(str(round((last_filled_line + i + 2) / 10000 * 100, 2)) + '% Done')


def get_anime_ids():
    import csv
    import codecs

    anime_ids = []
    with codecs.open('anime-list.csv', 'r', 'utf_8_sig') as anime_list:
        reader = csv.reader(anime_list)
        next(reader)
        for line in reader:
            anime_ids.append(line[0])

    return anime_ids


def get_anime_links():
    import csv
    import codecs

    anime_links = []
    with codecs.open('anime-list.csv', 'r', 'utf_8_sig') as anime_list:
        reader = csv.reader(anime_list)
        next(reader)
        for line in reader:
            anime_links.append(line[2])

    return anime_links


def is_not_found(page):
    message_field = page.find('p', class_='message')
    if message_field:
        return True
    else:
        return False


def get_ratings_for(link):
    anime_user_ratings = []

    ind = 0
    while len(anime_user_ratings) < 1000:
        print('Parsing page ' + str(ind + 1) + ', got ' + str(len(anime_user_ratings)) + ' ratings')
        anime_stats_html = requests.get(link + '/stats?show=' + str(ind * 75)).text
        stats_page = BeautifulSoup(anime_stats_html, 'lxml')
        ind += 1

        if not is_not_found(stats_page):
            ratings_table = stats_page.find('table', class_="table-recently-updated")
            user_lines = ratings_table.find_all('tr')
            user_lines = user_lines[1::]

            for user_line in user_lines:
                user_info = user_line.find('td', class_="borderClass di-t w100").find('div', class_="di-tc va-m al pl4")
                user_name = user_info.a.text

                score_field = user_line.find('td', class_="borderClass ac")
                user_rating = score_field.text

                anime_id = link.split('/')[4]

                if user_rating != '-':
                    record = [anime_id, user_name, user_rating]
                    anime_user_ratings.append(record)

        else:
            print('Page not found')
            break

        if len(anime_user_ratings) < 10 and ind > 20:
            print('No ratings found')
            break
    return anime_user_ratings


def are_ratings_done(complete_list):
    for anime in complete_list:
        if not complete_list[anime]:
            return False
    return True


def get_link_by_id(anime_id):
    anime_ids = get_anime_ids()
    anime_links = get_anime_links()
    return anime_links[anime_ids.index(anime_id)]


def fill_ratings_file():
    import csv
    import codecs

    with open('ratings-names.csv', 'r') as ratings_file:
        lines = ratings_file.readlines()
        lines_filled = len(lines)
    
    if lines_filled < 5:
        with open('ratings-names.csv', 'w', newline='') as ratings_file:
            writer = csv.writer(ratings_file)
            writer.writerow(['anime_id', 'user_name', 'rating'])

    anime_ids = get_anime_ids()
    complete_list = {}
    for anime_id in anime_ids:
        complete_list[anime_id] = False

    with codecs.open('ratings-names.csv', 'r', 'utf_8_sig') as ratings_file:
        reader = csv.reader(ratings_file)
        next(reader)
        for line in reader:
            anime_id = line[0]
            complete_list[anime_id] = True

    next_anime_id = anime_ids[0]
    while not are_ratings_done(complete_list):
        for anime_id in anime_ids:
            if not complete_list[anime_id]:
                next_anime_id = anime_id
                break

        next_anime_link = get_link_by_id(next_anime_id)
        print(f'Parsing {next_anime_link}')
        try:
            ratings = get_ratings_for(next_anime_link)

            with open('ratings-names.csv', 'a', encoding='utf_8_sig', newline='') as ratings_file:
                writer = csv.writer(ratings_file)
                writer.writerows(ratings)
                print(f'Got {len(ratings)} ratings')
                complete_list[next_anime_id] = True
        except AttributeError:
            import time
            time.sleep(60)


if __name__ == '__main__':
    fill_ratings_file()
