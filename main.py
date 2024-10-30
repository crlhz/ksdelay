from dotenv import load_dotenv
import os
import pickle
import logging

from scrapper import Scrapper
from message import Message
from bot import Bot

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='UTF-8'
)

old_messages = []
messages = []
unsent_messages = []

scrapper = Scrapper("https://www.kolejeslaskie.com/category/informacje/")
raw_messages = scrapper.get_data()

load_dotenv()
bot = Bot(os.getenv('BOT_TOKEN'))

for mes in raw_messages:
    message = Message(mes)
    if message.get_status() == 1:
        messages.append(message)
        logging.info("Recognized: " + message.get_data())
    else:
        logging.warning("Not recognized: " + message.get_data())

try:
    with open('old-messages.pkl', 'rb') as f:
        old_messages = pickle.load(f)
except (IOError, pickle.PickleError) as e:
    logging.error(f"Wystąpił błąd podczas zapisywania danych: {e}")

unsent_messages = set(messages) - set(old_messages)

for mes in unsent_messages:
    print(mes.get_data())
    bot.send_message(os.getenv("CHANNEL_ID"), mes.get_data())
print("***Koniec nowych wiadomości***")

with open('old-messages.pkl', 'wb') as f:
    pickle.dump(messages, f)
