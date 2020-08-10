from bs4 import BeautifulSoup
import requests

def get_anime_list():
    anime_list = []

    for i in range(200):
        print(str(((i + 1) / 200 * 100)) + '% Done')

        anime_top_html = requests.get('https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(i * 50)).text
        anime_top = BeautifulSoup(anime_top_html, 'lxml')
        for anime_paragraph in anime_top.find_all('div', class_='detail'):
            anime_paragraph = anime_paragraph.find('div', class_='di-ib clearfix')
            info = anime_paragraph.find('a', class_='hoverinfo_trigger fl-l fs14 fw-b')
            anime_name = None
            anime_id = None
            anime_link = None
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


if __name__ == '__main__':
    get_anime_list()