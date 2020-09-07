import telebot
from telebot import types
from telebot.types import Message
import config
from add_anime_functionality import add_anime
import db_communicator as db


bot = telebot.TeleBot(config.API_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    db.check_user(message)
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
    bot.send_message(message.chat.id, 'What do you want me to do?', reply_markup=markup)


@bot.message_handler()
def handle_any_message(message: Message):
    db.check_user(message)

    if message.text == 'Add anime':
        add_anime(message, bot)
    else:
        db.check_user(message)


bot.polling(none_stop=True)
