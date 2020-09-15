from telebot.types import Message
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import db_communicator as db
import search
import variables


def get_info(message: Message, bot=None):
    markup = types.ForceReply(selective=False)
    user_answer = bot.send_message(message.chat.id, 'What anime do you want to know about?', reply_markup=markup)
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
    exit_button = types.KeyboardButton('Exit info mode')
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
        markup = variables.main_menu()
        bot.send_message(message.chat.id, 'Information:', reply_markup=markup)
        message_text = ""
        title = db.get_first_title(searched_anime_id)
        anime_meta = db.get_meta_by_id(searched_anime_id)
        alternative_titles = anime_meta['titles'].split(',')
        if len(alternative_titles) > 1:
            alternative_titles = alternative_titles[1::]
        else:
            alternative_titles = []
        genres = ', '.join(anime_meta['genres'].split(','))
        rating = anime_meta['rating']
        members = db.convert_number_to_readable(anime_meta['members'])
        episodes = anime_meta['episodes']
        duration = anime_meta['duration']
        release_date = anime_meta['release_date']
        related_ids = list(map(int, anime_meta['related'].split(',')))
        message_text += f"<b>{title}</b>"
        if len(alternative_titles) > 0:
            message_text += '\n\nAlternative titles:'
            for alternative_title in alternative_titles:
                message_text += f'\n{alternative_title}'

        message_text += f'\n\nYear: <b>{release_date}</b>'
        message_text += f'\nRating: <b>{rating}</b>'
        message_text += f'\nViews: {members}'
        message_text += f'\n\nGenres:\n{genres}'
        message_text += f'\n\nEpisodes: {episodes}'
        message_text += f'\nEpisode duration: {duration} min(s)'

        real_related_ids = []
        for related_id in related_ids:
            if db.check_anime(related_id):
                real_related_ids.append(related_id)
        related_ids = real_related_ids
        if len(related_ids) > 0:
            message_text += '\n\nRelated to:'
            for related_id in related_ids:
                related_title = db.get_first_title(related_id)
                message_text += f'\n{related_title}'

        anime_poster = db.get_poster(searched_anime_id)

        inline_keyboard = InlineKeyboardMarkup(row_width=1)
        rate_button = InlineKeyboardButton(text='Rate', callback_data=f'rate-{searched_anime_id}-{message.chat.id}')
        ban_button = InlineKeyboardButton(text='Ban', callback_data=f'ban-{searched_anime_id}-{message.chat.id}')
        inline_keyboard.add(ban_button, rate_button)

        if anime_poster and len(message_text) <= 1020:
            bot.send_photo(message.chat.id, anime_poster, caption=message_text, reply_markup=inline_keyboard)
        else:
            if anime_poster:
                bot.send_photo(message.chat.id, anime_poster)
                bot.send_message(message.chat.id, message_text, reply_markup=inline_keyboard)
            else:
                bot.send_message(message.chat.id, message_text, reply_markup=inline_keyboard)

    elif message.text == 'Exit info mode':
        markup = variables.main_menu()
        bot.send_message(message.chat.id, 'Ok, leaving info mode', reply_markup=markup)
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
