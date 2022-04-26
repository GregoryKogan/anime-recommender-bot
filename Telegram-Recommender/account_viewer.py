import json
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import db_communicator as db


def show_account(message: Message, bot=None):
    user_id = message.from_user.id
    user_name, _ = db.get_user_data(user_id)
    user_ratings = db.get_ratings_by(user_id)
    user_ratings = json.loads(user_ratings) if user_ratings else {}
    message_text = f"<b>{user_name}</b>'s account"
    empty_account = True
    watched_ids = list(user_ratings)
    rating_list = []
    for watched_id in watched_ids:
        record = [user_ratings[watched_id], int(watched_id)]
        rating_list.append(record)
    rating_list.sort(reverse=True)
    if rating_list:
        empty_account = False
        message_text += "\n\nRatings: "
        for record in rating_list:
            rating = record[0]
            anime_id = record[1]
            title = db.get_meta_by_id(anime_id)['titles'].split(',')[0]
            line = f"\n○ {rating} - {title}"
            message_text += line
        last_line = f"\nYou've rated {len(rating_list)} titles"
        message_text += last_line

    user_ban_list = db.get_ban_list(user_id)
    if user_ban_list:
        empty_account = False
        message_text += "\n\nBan list:"
        for banned_id in user_ban_list:
            banned_title = db.get_first_title(banned_id)
            message_text += f"\n○ {banned_title}"
        message_text += f"\nYou've banned {len(user_ban_list)} titles"

    if empty_account:
        message_text += "\n\nYou don't have anything here yet"

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    remove_rating_button = InlineKeyboardButton(text='Remove rating',
                                                callback_data=f'remove_rating-{user_id}')
    remove_from_ban_list_button = InlineKeyboardButton(text='Remove from ban list',
                                                       callback_data=f'remove_from_ban_list-{user_id}')
    change_rating_button = InlineKeyboardButton(text='Change rating', 
                                                callback_data=f'change_rating-{user_id}')
    user_ratings = db.get_ratings_by(user_id)
    user_ratings = json.loads(user_ratings) if user_ratings else {}
    if list(user_ratings):
        inline_keyboard.add(remove_rating_button, change_rating_button)
    user_ban_list = db.get_ban_list(user_id)
    if not user_ban_list:
        user_ban_list = []
    if len(user_ban_list) > 0:
        inline_keyboard.add(remove_from_ban_list_button)
    if not empty_account:
        bot.send_message(message.chat.id, message_text, reply_markup=inline_keyboard)
    else:
        bot.send_message(message.chat.id, message_text)
