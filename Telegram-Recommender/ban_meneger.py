import db_communicator as db


def ban_anime(anime_id, chat_id, bot=None):
    user_id = db.get_user_id_by_chat_id(chat_id)
    db.ban_anime(user_id, anime_id)
    ban_title = db.get_first_title(anime_id)
    message_text = f"<b>{ban_title}</b> will no longer appear in your recommendations"
    bot.send_message(chat_id, message_text)
