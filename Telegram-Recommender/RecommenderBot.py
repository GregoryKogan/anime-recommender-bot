import telebot
from telebot.types import Message
import config
import db_communicator as db
import variables
from account_viewer import show_account
from add_anime_functionality import add_anime
from recommender import recommend


bot = telebot.TeleBot(config.API_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    db.check_user(message)
    markup = variables.main_menu()
    bot.send_message(message.chat.id, 'What do you want me to do?', reply_markup=markup)


@bot.message_handler()
def handle_any_message(message: Message):
    db.check_user(message)

    if message.text == 'Add anime':
        add_anime(message, bot)
    elif message.text == 'Get recommendations':
        chat_id = message.chat.id
        recommend(chat_id, 0, bot)
    elif message.text == 'Account':
        show_account(message, bot)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data.startswith('next'):
            recommendation_index = int(call.data.split('-')[1])
            recommend(call.message.chat.id, recommendation_index, bot)


bot.polling(none_stop=True)
