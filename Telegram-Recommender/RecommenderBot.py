import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.API_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
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
    bot.send_message(message.chat.id, '-=-=--=-=-=-', reply_markup=markup)


bot.polling()
