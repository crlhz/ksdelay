import telebot


class Bot:
    """
    Representation of telegram bot

    """

    def __init__(self, token):
        """
        Bot class constructor

        @param token: Bot token
        """
        self.token = token
        self.bot = telebot.TeleBot(token)

    def send_message(self, channel, message):
        """
        Sent message to the specific channel

        @param channel: Telegram channel ID
        @param message: Message content
        """
        try:
            self.bot.send_message(channel, message)
        except Exception as e:
            print(f"Błąd przy wysyłaniu wiadomości: {e}")
