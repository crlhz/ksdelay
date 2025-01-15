import json

from dotenv import load_dotenv
import os
import pickle
import logging
from logging.handlers import TimedRotatingFileHandler

from scrapper import Scrapper
from message import Message
from bot import Bot

handler = TimedRotatingFileHandler("timed_app.log", when="midnight", interval=1, backupCount=7)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='UTF-8',
)
logger = logging.getLogger("Logger")
logger.addHandler(handler)

old_messages = []
messages = []
unsent_messages = []

# get raw data from webpage
scrapper = Scrapper("https://www.kolejeslaskie.com/category/informacje/")
raw_messages = scrapper.get_data()

# initialize telegram bot
load_dotenv()
CHANNEL_IDS = json.loads(os.getenv("CHANNEL_IDS"))
bot = Bot(os.getenv('BOT_TOKEN'))

# convert raw data into messages
for mes in raw_messages:
    message = Message(mes)
    if message.get_status() == 1:
        messages.append(message)
        logging.info("Recognized: " + message.get_data())
    else:
        logging.warning("Not recognized: " + message.get_data())

# take old messages
try:
    with open('old-messages.pkl', 'rb') as f:
        old_messages = pickle.load(f)
except (IOError, pickle.PickleError) as e:
    logging.error(f"Wystąpił błąd podczas zapisywania danych: {e}")

# compare new messages with old messages
unsent_messages = set(messages) - set(old_messages)

# send messages that haven't been sent yet
for mes in unsent_messages:
    print(mes.get_data())
    bot.send_message(CHANNEL_IDS[mes.get_line(mes.get_number())], mes.get_data())
print("***Koniec nowych wiadomości***")

# save new messages as old messages
with open('old-messages.pkl', 'wb') as f:
    pickle.dump(messages, f)
