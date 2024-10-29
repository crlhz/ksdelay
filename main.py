import time
from dotenv import load_dotenv
import os

from scrapper import Scrapper
from message import Message
from bot import Bot


scrapper = Scrapper("https://www.kolejeslaskie.com/category/informacje/")
raw_messages = scrapper.get_data()

old_messages = []
messages = []
unsent_messages = []

load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))

while True:
    scrapper = Scrapper("https://www.kolejeslaskie.com/category/informacje/")
    raw_messages = scrapper.get_data()
    for mes in raw_messages:
        message = Message(mes)
        if message.get_status() == 1:
            messages.append(message)

    unsent_messages = set(messages) - set(old_messages)
    for mes in unsent_messages:
        print(mes.get_data())
        bot.send_message(os.getenv("CHANNEL_ID"), mes.get_data())
    print("***Koniec nowych wiadomości***")
    old_messages = messages.copy()
    messages.clear()
    raw_messages.clear()
    time.sleep(600)