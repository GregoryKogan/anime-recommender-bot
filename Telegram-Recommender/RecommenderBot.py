import telebot
from telebot.types import Message
import config
import db_communicator as db
from account_viewer import show_account
from add_anime_functionality import add_anime, add_rating_from_inline
from ban_meneger import ban_anime
from help_message import send_help
from info_show import get_info
from recommender import recommend
from remove_from_ban_list_functionality import remove_from_ban_list
from remove_rating import remove_rating_for
from errror_handler import handle_error

bot = telebot.TeleBot(config.API_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    try:
        db.check_user(message)
        user_name = db.get_user_name(message)
        bot.send_message(message.chat.id, f"Hello, {user_name}!")
        send_help(message, bot)
    except Exception as error:
        handle_error(error, message.chat.id, bot)


@bot.message_handler(commands=['help'])
def handle_help(message: Message):
    try:
        db.check_user(message)
        send_help(message, bot)
    except Exception as error:
        handle_error(error, message.chat.id, bot)


@bot.message_handler(commands=['rateanime'])
def handle_rate(message: Message):
    try:
        db.check_user(message)
        add_anime(message, bot)
    except Exception as error:
        handle_error(error, message.chat.id, bot)


@bot.message_handler(commands=['account'])
def handle_account(message: Message):
    try:
        db.check_user(message)
        show_account(message, bot)
    except Exception as error:
        handle_error(error, message.chat.id, bot)


@bot.message_handler(commands=['getrecs'])
def handle_recs(message: Message):
    try:
        db.check_user(message)
        chat_id = message.chat.id
        recommend(chat_id, 0, bot)
    except Exception as error:
        handle_error(error, message.chat.id, bot)


@bot.message_handler(commands=['info'])
def handle_account(message: Message):
    try:
        db.check_user(message)
        get_info(message, bot)
    except Exception as error:
        handle_error(error, message.chat.id, bot)


@bot.message_handler()
def handle_any_message(message: Message):
    try:
        db.check_user(message)

        if message.text == 'Rate anime':
            add_anime(message, bot)
        elif message.text == 'Get recommendations':
            chat_id = message.chat.id
            recommend(chat_id, 0, bot)
        elif message.text == 'Account':
            show_account(message, bot)
        elif message.text == 'Info':
            get_info(message, bot)
    except Exception as error:
        handle_error(error, message.chat.id, bot)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data.startswith('next'):
                recommendation_index = int(call.data.split('-')[1])
                recommend(call.message.chat.id, recommendation_index, bot)
            elif call.data.startswith('rate'):
                anime_id, chat_id = call.data.split('-')[1::]
                add_rating_from_inline(anime_id, chat_id, bot)
            elif call.data.startswith('ban'):
                anime_id, chat_id = call.data.split('-')[1::]
                ban_anime(anime_id, chat_id, bot)
            elif call.data.startswith('remove_rating'):
                user_id = call.data.split('-')[1]
                remove_rating_for(user_id, bot)
            elif call.data.startswith('remove_from_ban_list'):
                user_id = call.data.split('-')[1]
                remove_from_ban_list(user_id, bot)
            else:
                print(call.data)
    except Exception as error:
        handle_error(error, call.message.chat.id, bot)


bot.polling(none_stop=True)
