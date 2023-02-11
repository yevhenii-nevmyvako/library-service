import os
import telebot
from dotenv import load_dotenv


load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=["start", "help", "paid"])
def send_message(message):
    bot.reply_to(message, "text-message")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
