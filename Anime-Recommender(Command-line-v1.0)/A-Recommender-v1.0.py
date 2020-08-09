import Recommender
import Search


def help_user():
    print('''
====================================================
           This is Anime Recommender v1.0
----------------------------------------------------
    
Find anime titles you've watched and rate them,
you can get personal anime recommendations based on
your ratings!
    
Commands:
'help'      - get short description and possible commands list
'account'   - view your ratings
'ban list'  - view your ban list
'add anime' - rate new anime title
'ban anime' - never recommend this anime
'get recs'  - get personal recommendations
'exit'      - exit application
    
'account clear'  - erase all ratings you currently have 
'ban list clear' - clear all bans you did
    
------------------------
2020 G.Koganovkiy
====================================================
''')


def sort_user_ratings():
    import csv
    import codecs
    user_file = codecs.open('user.csv', 'r', 'utf_8_sig')
    reader = csv.reader(user_file)
    next(reader)
    data = []
    for line in reader:
        anime_id = line[0]
        user_rating = float(line[1])
        record = [user_rating, anime_id]
        data.append(record)
    data.sort()
    data.reverse()
    user_file.close()
    user_file = codecs.open('user.csv', 'w', 'utf_8_sig')
    writer = csv.writer(user_file)
    writer.writerow(['anime_id', 'rating'])
    for record in data:
        writer.writerow([record[1], record[0]])
    user_file.close()


def update_user(user):
    import csv
    import codecs
    user_file = codecs.open('user.csv', 'w', 'utf_8_sig')
    writer = csv.writer(user_file)
    writer.writerow(['anime_id', 'rating'])
    for anime in user:
        writer.writerow([anime, user[anime]])
    user_file.close()


def get_ban_list():
    import csv
    import codecs
    ban_file = codecs.open('banned.csv', 'r', 'utf_8_sig')
    reader = csv.reader(ban_file)
    next(reader)
    ban_list = []
    for line in reader:
        ban_list.append(line[0])
    ban_file.close()
    return ban_list


def get_new_user_rating():
    titles_list = Search.get_titles()
    user_rating = None

    title_added = False
    while not title_added:
        user_input = str(input('Find title: '))

        if user_input == 'stop':
            return 'Nothing added'

        best_fit = Search.find(user_input, titles_list.copy())
        if best_fit == 'Not Found':
            print(best_fit)
            continue
        anime_name = best_fit[0]

        answer_received = False
        user_answer = None
        while not answer_received:
            user_answer = str(input('Is it ' + anime_name + '? - '))
            if user_answer == 'no' or user_answer == 'yes':
                answer_received = True
            else:
                print("Type 'yes' or 'no'")
        if user_answer == 'no':
            continue
        elif user_answer == 'yes':
            user_rating = float(input('Your rating for ' + anime_name + ': '))

        user_rating = [Search.get_id_by_name(anime_name), user_rating]
        title_added = True
    return user_rating


def find_title():
    titles_list = Search.get_titles()
    banned_anime = None

    title_added = False
    while not title_added:
        user_input = str(input('Find title: '))

        if user_input == 'stop':
            return 'Nothing banned'

        best_fit = Search.find(user_input, titles_list.copy())
        if best_fit == 'Not Found':
            print(best_fit)
            continue
        anime_name = best_fit[0]

        answer_received = False
        user_answer = None
        while not answer_received:
            user_answer = str(input('Is it ' + anime_name + '? - '))
            if user_answer == 'no' or user_answer == 'yes':
                answer_received = True
            else:
                print("Type 'yes' or 'no'")
        if user_answer == 'no':
            continue
        elif user_answer == 'yes':
            banned_anime = Search.get_id_by_name(anime_name)
            title_added = True

    return banned_anime


def get_user_ratings():
    user_ratings = []

    import csv
    import codecs
    user_file = codecs.open('user.csv', 'r', 'utf_8_sig')
    reader = csv.reader(user_file)

    next(reader)

    for line in reader:
        anime_id = line[0]
        user_rating = float(line[1])
        review = [anime_id, user_rating]
        user_ratings.append(review)

    user_file.close()
    return user_ratings


def add_anime():
    new_rating = get_new_user_rating()
    if new_rating != 'Nothing added':
        user = Search.get_user_data()
        user[new_rating[0]] = new_rating[1]
        update_user(user)
        print('Anime successfully added')


def ban_anime():
    banned_anime = find_title()
    if banned_anime != 'Nothing banned':
        import csv
        import codecs
        ban_file = codecs.open('banned.csv', 'r', 'utf_8_sig')
        reader = csv.reader(ban_file)
        data = []
        for line in reader:
            data.append(line)
        ban_file.close()

        ban_file = codecs.open('banned.csv', 'w', 'utf_8_sig')
        writer = csv.writer(ban_file)
        data.append([str(banned_anime)])
        writer.writerows(data)
        ban_file.close()
        print('Anime successfully banned')


def get_recommendations():
    user_data = get_user_ratings()

    anime_ids = Recommender.get_line('RecommenderDB.csv', 0)
    anime_ids.pop(0)
    anime_ratings = Recommender.get_anime_ratings()

    recommendations = Recommender.get_empty_recommendations_object(anime_ids)

    for review in user_data:
        anime_id = review[0]
        user_rating = review[1]
        line_in_db = anime_ids.index(anime_id) + 1
        coefficients = Recommender.get_line('RecommenderDB.csv', line_in_db)
        coefficients.pop(0)
        for i, coefficient in enumerate(coefficients):
            second_anime_id = anime_ids[i]
            crowd_rating = anime_ratings[second_anime_id]
            score = float(coefficient) * user_rating * crowd_rating
            recommendations[second_anime_id] += score

    recommendation_list = Recommender.convert_to_recommendation_list(recommendations)

    ind = 0
    while ind < len(recommendation_list):
        for user_rating in user_data:
            if recommendation_list[ind][1] == user_rating[0]:
                recommendation_list.pop(ind)
                ind -= 1
        ind += 1

    ban_list = get_ban_list()
    ind = 0
    while ind < len(recommendation_list):
        for banned_anime in ban_list:
            if recommendation_list[ind][1] == banned_anime:
                recommendation_list.pop(ind)
                ind -= 1
        ind += 1

    return recommendation_list


def clear_account():
    import csv
    import codecs
    user_file = codecs.open('user.csv', 'w', 'utf_8_sig')
    writer = csv.writer(user_file)
    writer.writerow(['anime_id', 'rating'])
    user_file.close()
    print('Account ratings erased')


def clear_ban_list():
    import csv
    import codecs
    ban_file = codecs.open('banned.csv', 'w', 'utf_8_sig')
    writer = csv.writer(ban_file)
    writer.writerow(['anime_id'])
    ban_file.close()
    print('Ban list is now empty')


def manage_user_input(user_input):
    if user_input == 'help':
        help_user()
    elif user_input == 'exit':
        print('----------------------------------------------------')
        global running
        running = False
    elif user_input == 'account':
        sort_user_ratings()
        user = Search.get_user_data()
        if len(user) > 0:
            print('Your ratings: ')
            for anime in user:
                print(Recommender.get_name_by_id(anime) + ' - ' + str(user[anime]))
        else:
            print("You don't have any reviews currently")
    elif user_input == 'ban list':
        ban_list = get_ban_list()
        if len(ban_list) > 0:
            print('Banned titles:')
            for anime in ban_list:
                print(Recommender.get_name_by_id(anime))
        else:
            print("You didn't ban anything yet")
    elif user_input == 'add anime':
        print("Type 'stop' to exit add mode")
        add_anime()
    elif user_input == 'get recs':
        recommendations = get_recommendations()

        if len(recommendations) == 0:
            print("Can't give recommendations")

        for i in range(min(10, len(recommendations))):
            print(str(i + 1) + ') ' + 'Score: ' + str(int(recommendations[i][0])) + ' - '
                  + Recommender.get_name_by_id(recommendations[i][1]))
    elif user_input == 'ban anime':
        print("Type 'stop' to exit ban mode")
        ban_anime()
    elif user_input == 'account clear':
        clear_account()
    elif user_input == 'ban list clear':
        clear_ban_list()
    else:
        if user_input != '':
            print("There is no '" + user_input + "' command")


if __name__ == '__main__':
    print("Use 'help' command to get commands list")
    running = True
    while running:
        user_input = str(input())
        manage_user_input(user_input)
