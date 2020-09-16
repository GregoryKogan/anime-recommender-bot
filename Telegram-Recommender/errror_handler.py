def handle_error(error, chat_id, bot):
    bot.send_message(chat_id, """Ooops! Your last action somehow broke this bot. 
    You can contact <a href="tg://user?id=544711957">me</a> for bug report""")
    print(error)

