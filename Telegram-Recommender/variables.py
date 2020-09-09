from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, selective=False)
    add_anime_button = types.KeyboardButton('Add anime')
    ban_anime_button = types.KeyboardButton('Ban Anime')
    account_button = types.KeyboardButton('Account')
    ban_list_button = types.KeyboardButton('Ban list')
    get_recs_button = types.KeyboardButton('Get recommendations')
    markup.add(add_anime_button,
               ban_anime_button,
               account_button,
               ban_list_button,
               get_recs_button)
    return markup
