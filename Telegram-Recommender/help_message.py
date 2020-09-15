from telebot.types import Message
import variables


def send_help(message: Message, bot=None):
    message_text \
        = """
Anime Recommender v3.0

This bot gives you personalized recommendations based on your ratings!

Commands:
    ○ /start - begin messaging
    ○ /help - get description and list of commands
    ○ /rateanime - set your rating for anime
    ○ /account - view your account information
    ○ /getrecs - get personalized recommendations
    ○ /info - get information about any anime

More detailed information about how this system works is on <a href="github.com/GregoryKogan/Anime-Recommender">github</a>
For bug report or other contact <a href="tg://user?id=544711957">me</a>
"""
    markup = variables.main_menu()
    bot.send_message(message.chat.id, message_text, reply_markup=markup, disable_web_page_preview=True)
    bot.send_message(message.chat.id, 'What do you want me to do?')
