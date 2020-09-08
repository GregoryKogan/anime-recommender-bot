import telebot
from telebot import types
from telebot.types import Message
import search
import db_communicator as db


def add_anime(message: Message, bot):
    markup = types.ForceReply(selective=False)
    user_answer = bot.send_message(message.chat.id, 'Find title:', reply_markup=markup)
    bot.register_next_step_handler(user_answer, find_anime, bot=bot)


def find_anime(message: Message, bot=None):
    search_result = search.find(message.text)[0]
    titles = db.get_meta_by_id(search_result)['titles'].split(',')
    message_text = f"""Is it <b>{titles[0]}</b>?\n\n"""
    if len(titles) > 1:
        message_text += 'Alternative titles:\n'
        for title_ind in range(1, len(titles)):
            message_text += f'{titles[title_ind]}\n'
    markup = types.ReplyKeyboardMarkup(row_width=2)
    yes_button = types.KeyboardButton('Yes')
    no_button = types.KeyboardButton('No')
    markup.add(no_button, yes_button)
    user_answer = bot.send_message(message.chat.id, message_text, reply_markup=markup)
    bot.register_next_step_handler(user_answer, process_user_search_answer, search_result, bot=bot)


def process_user_search_answer(message: Message, searched_anime_id, bot=None):
    if message.text == 'No':
        markup = types.ForceReply(selective=False)
        message_text = """Ok, try again
Find title:"""
        user_answer = bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(user_answer, find_anime, bot=bot)
    elif message.text == 'Yes':
        title = db.get_meta_by_id(searched_anime_id)['titles'].split(',')[0]
        message_text = f"Your rating (from 0 to 10) for <b>{title}</b>:"
        markup = types.ForceReply(selective=False)
        user_answer = bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(user_answer, receive_user_rating, searched_anime_id, bot=bot)
    else:
        second_message_text = "<b>Please, tell me 'Yes' or 'No'!</b>"
        titles = db.get_meta_by_id(searched_anime_id)['titles'].split(',')
        first_message_text = f"""Is it <b>{titles[0]}</b>?\n\n"""
        if len(titles) > 1:
            first_message_text += 'Alternative titles:\n'
            for title_ind in range(1, len(titles)):
                first_message_text += f'{titles[title_ind]}\n'
        markup = types.ReplyKeyboardMarkup(row_width=2, selective=False)
        yes_button = types.KeyboardButton('Yes')
        no_button = types.KeyboardButton('No')
        markup.add(no_button, yes_button)
        bot.send_message(message.chat.id, first_message_text)
        user_answer = bot.send_message(message.chat.id, second_message_text, reply_markup=markup)
        bot.register_next_step_handler(user_answer, process_user_search_answer, searched_anime_id, bot=bot)


def receive_user_rating(message: Message, anime_id, bot=None):
    rating = None
    try:
        rating = float(message.text)
    except ValueError:
        pass
    title = db.get_meta_by_id(anime_id)['titles'].split(',')[0]
    if rating and 0 <= rating <= 10:
        user_id = message.from_user.id
        db.add_rating(user_id, anime_id, rating)
        db.update_factors(user_id)
        message_text = f"Rating <b>{rating}</b> for <b>{title}</b> successfully added to your account!"
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
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
    else:
        message_text = "<b>Rating must be a number from 0 to 10!</b>"
        message_text += f"\nYour rating for <b>{title}</b>:"
        markup = types.ForceReply(selective=False)
        user_answer = bot.send_message(message.chat.id, message_text, reply_markup=markup)
        bot.register_next_step_handler(user_answer, receive_user_rating, anime_id, bot=bot)