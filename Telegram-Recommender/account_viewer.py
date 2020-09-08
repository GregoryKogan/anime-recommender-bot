import json
from telebot.types import Message
import db_communicator as db


def show_account(message: Message, bot=None):
    user_id = message.from_user.id
    user_name, _ = db.get_user_data(user_id)
    user_ratings = json.loads(db.get_ratings_by(user_id))
    message_text = f"<b>{user_name}</b>'s account"
    message_text += "\n\nRatings: "
    watched_ids = list(user_ratings)
    rating_list = []
    for watched_id in watched_ids:
        record = [user_ratings[watched_id], int(watched_id)]
        rating_list.append(record)
    rating_list.sort(reverse=True)
    for record in rating_list:
        rating = record[0]
        anime_id = record[1]
        title = db.get_meta_by_id(anime_id)['titles'].split(',')[0]
        line = f"\n○ {rating} - {title}"
        message_text += line
    last_line = f"\n\nYou've rated {len(rating_list)} titles"
    message_text += last_line
    bot.send_message(message.chat.id, message_text)
