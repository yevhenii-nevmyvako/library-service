import os
import telebot
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(token=token)
chat_id = os.getenv("TELEGRAM_CHAT_ID")


def send_message(message: str) -> object:
    return bot.send_message(chat_id, message)
