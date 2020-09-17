from telebot import types


HELLO_STICKER_ID = 'CAACAgIAAxkBAAIHtF9jiqrGwzZ8jkfHTMN3fslM4N5yAALdhAEAAWOLRgxOav1fhlRd8hsE'
FLEX_STICKER_ID = 'CAACAgIAAxkBAAIHtV9jirr1N3qR-c2VEw_ZszVcqlYjAALUhAEAAWOLRgx8mO44WEM-RBsE'
CRYING_STICKER_ID = 'CAACAgIAAxkBAAIHtl9jisfZTwYD51Cc5mCoyAskGrjGAALahAEAAWOLRgyb_IGWiVVcQBsE'
DANCING_STICKER_ID = 'CAACAgIAAxkBAAIHt19jitNkbFlypMthvlH7JpwZwCkjAALbhAEAAWOLRgyGneVm_SwRkBsE'
APPROVAL_STICKER_ID = 'CAACAgIAAxkBAAIHqV9jiVySW7UhusyoDh7GS1wfpG5fAALchAEAAWOLRgx__Vi-UO5D5BsE'


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
