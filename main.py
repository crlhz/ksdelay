import time

from scrapper import Scrapper
from message import Message

scrapper = Scrapper("https://www.kolejeslaskie.com/category/informacje/")
raw_messages = scrapper.get_data()

old_messages = []
messages = []
unsent_messages = []

while True:
    scrapper = Scrapper("https://www.kolejeslaskie.com/category/informacje/")
    raw_messages = scrapper.get_data()
    for mes in raw_messages:
        message = Message(mes)
        if message.get_status() == 1:
            messages.append(message)

    unsent_messages = set(messages) - set(old_messages)
    for mes in unsent_messages:
        print(mes.get_route())
    print("***Koniec nowych wiadomości***")
    old_messages = messages
    messages.clear()
    raw_messages.clear()
    time.sleep(600)