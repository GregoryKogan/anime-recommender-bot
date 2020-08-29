import telebot
from telebot import types
from telebot.types import Message
import config
import db_communicator as db
import search

bot = telebot.TeleBot(config.API_TOKEN, parse_mode='HTML')


def reading_user_rating(message: Message, searched_anime_id):
    if db.is_number(message.text) and 0 <= float(message.text) <= 10.0:
        user_id = db.get_user_id_by_chat_id(message.chat.id)
        rating = float(message.text)
        db.add_anime_rating(user_id, rating, searched_anime_id)
        markup = types.ReplyKeyboardMarkup(row_width=1)
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
        bot.send_message(message.chat.id, f"Rating <b>{rating}</b> for "
                                          f"<b>{db.get_first_title_by_id(searched_anime_id)}</b> "
                                          f"successfully added to your account", reply_markup=markup)
    else:
        markup = types.ForceReply(selective=False)
        msg = bot.send_message(message.chat.id, f"""<b>Rating must be a number between 0 and 10</b>
Your rating for <b>{db.get_first_title_by_id(searched_anime_id)}</b>:""", reply_markup=markup)
        bot.register_next_step_handler(msg, reading_user_rating, searched_anime_id)


def process_user_answer_for_search(message: Message, searched_anime_id):
    if message.text == 'Yes':
        markup = types.ForceReply(selective=False)
        msg = bot.send_message(message.chat.id,
                               f'Your rating from 0 to 10 for <b>{db.get_first_title_by_id(searched_anime_id)}</b>:',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, reading_user_rating, searched_anime_id)
    else:
        markup = types.ForceReply(selective=False)
        msg = bot.send_message(message.chat.id, 'Try to find your title again:', reply_markup=markup)
        bot.register_next_step_handler(msg, find_anime)


def find_anime(message: Message):
    search_result = search.find(message.text)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    yes_button = types.KeyboardButton('Yes')
    no_button = types.KeyboardButton('No')
    markup.add(yes_button, no_button)
    msg = bot.send_message(message.chat.id,
                           f"Is it <b>{db.get_first_title_by_id(search_result[0])}</b>?", reply_markup=markup)
    bot.register_next_step_handler(msg, process_user_answer_for_search, search_result[0])


def add_anime(message: Message):
    if not db.get_user_data(message.from_user.id):
        db.add_user(message)

    markup = types.ForceReply(selective=False)
    msg = bot.send_message(message.chat.id, "Find title:", reply_markup=markup)
    bot.register_next_step_handler(msg, find_anime)


@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
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
    bot.send_message(message.chat.id, 'What do you want me to do?', reply_markup=markup)


@bot.message_handler()
def handle_any_message(message: Message):
    if message.text == 'Add anime':
        add_anime(message)


bot.polling(none_stop=True)
