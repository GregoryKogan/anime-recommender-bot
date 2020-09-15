from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, selective=False)
    add_anime_button = types.KeyboardButton('Rate anime')
    account_button = types.KeyboardButton('Account')
    info_button = types.KeyboardButton('Info')
    get_recs_button = types.KeyboardButton('Get recommendations')
    markup.add(get_recs_button,
               add_anime_button,
               info_button,
               account_button)
    return markup
