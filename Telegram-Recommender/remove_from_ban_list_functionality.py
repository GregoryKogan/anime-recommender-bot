from telebot import types
from telebot.types import Message
import db_communicator as db
import search
import variables


def remove_from_ban_list(user_id, bot=None):
    _, chat_id = db.get_user_data(user_id)
    markup = types.ForceReply(selective=False)
    user_answer = bot.send_message(chat_id, 'Which anime do you want to remove?', reply_markup=markup)
    bot.register_next_step_handler(user_answer, find_anime, bot=bot)


def find_anime(message: Message, bot=None):
    search_guesses = search.find(message.text)[:6:]
    search_result = search_guesses.pop(0)
    message_text = ""
    if len(search_guesses) > 0:
        message_text += "<b>Perhaps you meant:</b>"
        for search_guess in search_guesses:
            related_title = db.get_first_title(search_guess)
            message_text += f'\n{related_title}'
        message_text += '\n\n'
    titles = db.get_meta_by_id(search_result)['titles'].split(',')
    message_text += f"Is it <b>{titles[0]}</b>?"
    release_date = db.get_meta_by_id(search_result)['release_date']
    message_text += f'\nYear: {release_date}\n\n'
    if len(titles) > 1:
        message_text += '<b>Alternative titles:</b>\n'
        for title_ind in range(1, len(titles)):
            message_text += f'{titles[title_ind]}\n'
    markup = types.ReplyKeyboardMarkup(row_width=2)
    yes_button = types.KeyboardButton('Yes')
    no_button = types.KeyboardButton('No')
    exit_button = types.KeyboardButton('Exit removing mode')
    markup.add(no_button, yes_button, exit_button)
    anime_poster = db.get_poster(search_result)
    if anime_poster:
        bot.send_photo(message.chat.id, anime_poster)
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
        removed_title = db.get_first_title(searched_anime_id)
        message_text = f"{removed_title} is no longer in your ban list"
        markup = variables.main_menu()
        user_id = message.from_user.id
        db.remove_ban(user_id, searched_anime_id)
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
    elif message.text == 'Exit removing mode':
        markup = variables.main_menu()
        bot.send_message(message.chat.id, 'Ok, leaving removing mode', reply_markup=markup)
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
