from bs4 import BeautifulSoup
import requests
import csv
import sqlite3


def get_page(link):
    response = requests.get(link).text
    page = BeautifulSoup(response, 'lxml')
    return page


def make_record_in_csv(file_name, record):
    with open(file_name, 'a', encoding='utf_8_sig', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(record)


def get_anime_list():
    make_record_in_csv('anime_list.csv', ['anime_id', 'anime_name', 'anime_link'])
    
    default_link = 'https://myanimelist.net/topanime.php?type=bypopularity&limit='
    for page_num in range(200):
        current_page = get_page(default_link + f'{page_num * 50}')
        ranking_lines = current_page.find_all('tr', class_='ranking-list')
        for ranking_line in ranking_lines:
            info_part = ranking_line.find('td', class_='title al va-t word-break')
            anime_link = info_part.find('a', class_='hoverinfo_trigger fl-l ml12 mr8')['href']
            anime_id = anime_link.split('/')[4]
            anime_name = anime_link.split('/')[5]
            make_record_in_csv('anime_list.csv', [anime_id, anime_name, anime_link])
            print(f'{page_num / 2}% Done: ', anime_id, anime_name, anime_link)


def get_meta(anime_id, anime_link):
    page = get_page(anime_link)
    anime_titles = []
    main_title = page.find('h1', class_='title-name').text
    anime_titles.append(main_title)
    sub_paragraphs = page.find_all('div', class_='spaceit_pad')
    alternative_titles = []
    for sub_paragraph in sub_paragraphs:
        span = sub_paragraph.span
        if span:
            if span.text == 'English:':
                eng_titles = sub_paragraph.text[len('English:  '):-3:].split(',')
                for title in eng_titles:
                    if title[0] == ' ':
                        title = title[1::]
                    alternative_titles.append(title)
            elif span.text == 'Synonyms:':
                syn_titles = sub_paragraph.text[len('Synonyms:  '):-3:].split(',')
                for title in syn_titles:
                    if len(title) > 0:
                        if title[0] == ' ':
                            title = title[1::]
                        alternative_titles.append(title)
    for alternative_title in alternative_titles:
        if alternative_title != main_title:
            anime_titles.append(alternative_title)

    anime_rating = page.find('div', class_='fl-l score').div.text

    anime_members = page.find('span', class_='numbers members').strong.text.replace(',', '')

    num_of_episodes = 1
    release_date = 2020
    duration = 24
    info_pads = page.find('td', class_='borderClass').find_all('div', class_='spaceit')
    for info_pad in info_pads:
        if info_pad.text.find('Episodes:') != -1:
            num_of_episodes = info_pad.text[len(' Episodes:   '):-3:]
        elif info_pad.text.find('Aired:') != -1:
            try:
                release_date = info_pad.text[len(' Aired:   ')::].split('to')[0].split(',')[1][1:-1:]
            except IndexError:
                pass
        elif info_pad.text.find('Duration:') != -1:
            duration = info_pad.text[len(' Duration:   ')::].split(' ')[0]

    anime_genres = []
    other_pads = page.find('td', class_='borderClass').find_all('div')
    for pad in other_pads:
        span = pad.find('span', class_='dark_text')
        if span:
            if span.text.find('Genres:') != -1:
                genre_pads = pad.find_all('span', itemprop='genre')
                for genre_pad in genre_pads:
                    anime_genres.append(genre_pad.text)

    related_titles = []
    try:
        related_table = page.find('table', class_='anime_detail_related_anime')
        related_pads = related_table.find_all('tr')
        for related_pad in related_pads:
            related_link = related_pad.find_all('td', class_='borderClass')[1].a['href']
            if related_link.startswith('/anime/'):
                related_id = related_link.split('/')[2]
                related_titles.append(related_id)
    except Exception as error:
        print(error)

    titles_string = ','.join(anime_titles)
    genres_string = ','.join(anime_genres)
    related_string = ','.join(related_titles)
    anime_id = int(anime_id)
    if anime_rating == 'N/A':
        anime_rating = 0.0
    else:
        anime_rating = float(anime_rating)
    anime_members = int(anime_members)
    if num_of_episodes == 'Unknown':
        num_of_episodes = 0
    else:
        num_of_episodes = int(num_of_episodes)
    if duration != 'Unknown\n':
        duration = int(duration)
    else:
        duration = 0
    release_date = int(release_date)
    # print(f'anime id: {anime_id}')
    # print(f'titles: {titles_string}')
    # print(f'genres: {genres_string}')
    # print(f'rating: {anime_rating}')
    # print(f'members: {anime_members}')
    # print(f'episodes: {num_of_episodes}')
    # print(f'duration: {duration}')
    # print(f'release date: {release_date}')
    # print(f'related: {related_string}')

    connection = sqlite3.connect('Recommender.db')
    executor = connection.cursor()
    executor.execute(f"""INSERT INTO anime_meta VALUES 
(:anime_id, :titles, :genres, :rating, :members, :episodes, :duration, :release_date, :related_ids)""",
                     {'anime_id': anime_id,
                      'titles': titles_string,
                      'genres': genres_string,
                      'rating': anime_rating,
                      'members': anime_members,
                      'episodes': num_of_episodes,
                      'duration': duration,
                      'release_date': release_date,
                      'related_ids': related_string})
    connection.commit()
    connection.close()


def fill_db():
    with open('anime_list.csv', mode='r', encoding='utf_8_sig') as anime_list_file:
        reader = csv.reader(anime_list_file)
        next(reader)
        anime_list = list(reader)

    for anime_record in anime_list:
        anime_id = anime_record[0]
        anime_link = anime_record[2]
        print(f'Parsing {anime_link}')
        done = False
        while not done:
            try:
                get_meta(anime_id, anime_link)
                done = True
            except Exception as error:
                print(error)


if __name__ == '__main__':
    fill_db()
