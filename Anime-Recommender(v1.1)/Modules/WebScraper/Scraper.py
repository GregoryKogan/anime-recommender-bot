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


def fill_meta_file():
    import csv
    import codecs

    anime_links = []
    with codecs.open('anime-list.csv', 'r', 'utf_8_sig') as anime_list:
        reader = csv.reader(anime_list)
        next(reader)
        for line in reader:
            anime_links.append(line[2])

    with codecs.open('anime-meta.csv', 'w', 'utf_8_sig') as meta_file:
        writer = csv.writer(meta_file)
        writer.writerow(['anime_id', 'titles', 'rating', 'members', 'genres'])

    for i, link in enumerate(anime_links):
        print(str(round((i + 1) / len(anime_links) * 100, 2)) + '% Done')

        meta_info = get_meta_info(link)
        with open('anime-meta.csv', 'a', newline='', encoding='utf_8_sig') as meta_file:
            writer = csv.writer(meta_file, delimiter=',', quotechar='"')
            writer.writerow(meta_info)


if __name__ == '__main__':
    fill_meta_file()
