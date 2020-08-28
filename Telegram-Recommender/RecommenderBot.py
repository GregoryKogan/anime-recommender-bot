import telebot
import config

bot = telebot.TeleBot(config.API_TOKEN)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f'Sup, {message.from_user.first_name}')
    print(f"""Message: {message.text}
Chat: {message.chat.id}
From: {message.from_user.username}""")


bot.polling()
