import os
import time
import telebot
from dotenv import load_dotenv

#
# class Bot:
#     def __init__(self):
#


load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


# Funkcja wysyłająca wiadomości
def send_test_message():
    try:
        bot.send_message(os.getenv('CHANNEL_ID'), "test")
    except Exception as e:
        print(f"Błąd przy wysyłaniu wiadomości: {e}")


# Pętla nieskończona do wysyłania wiadomości
while True:
    send_test_message()
    time.sleep(20)
