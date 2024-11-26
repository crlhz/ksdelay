import os
import re
from logging import exception

TRAIN_NUMBERS_PATH = "./train_numbers/"

class Message:
    """
    Representation of a single message

    """

    def __init__(self, data):
        """
        Message constructor

        @param data:     content of single message provided via parser
        """
        self.data = data
        self.status = 1
        self.sent = 0

        self.type = self.__parse_type(data)

        if self.type == "delayed" or "canceled":
            self.number = self.__parse_number(data)
            self.route = self.__parse_route(data)
            self.delay = self.__parse_delay(data)

    def __eq__(self, other):
        """
        Method necessary to compare two message instances

        @param other:   Object to compare
        @return:        False -> not equal
                        True  -> equal
        """
        if isinstance(other, Message):
            return self.data == other.data
        return False

    def __hash__(self):
        """
        Hash message's data, implemented for __eq__()

        @return:        Hashed message data
        """
        return hash(self.data)

    def get_status(self):
        """
        Status getter

        @return:        Message status
                        0 -> message incorrect
                        1 -> message correct
        """
        return self.status

    def get_type(self):
        """
        Type getter

        @return:        Message type, available:
                        - delayed
                        - cancelled
                        - not recognized
        """
        return self.type

    def get_number(self):
        """
        Number getter

        @return:        Train number
        """
        return self.number

    def get_route(self):
        """
        Route getter

        @return:        Train route as a dictionary
                        departure city  :   departure time
                        arrival city    :   arrival time
        """
        return self.route

    def get_delay(self):
        """
        Delay getter

        @return:        Train delay
        """
        return self.delay

    def get_data(self):
        """
        Data getter

        @return:        Message content
        """
        return self.data

    def is_sent(self):
        """
        Getter for sent status

        @return:        Message sent status
        """
        return self.sent

    def send(self):
        """
        Setter for sent status

        """
        self.sent = 1

    def get_line(self, train_number):
        """
        Getter for line using train number.

        @param train_number:    train number
        @return:                Line
        """
        files = [name for name in os.listdir(TRAIN_NUMBERS_PATH) if os.path.isfile(os.path.join(TRAIN_NUMBERS_PATH, name))]
        for file in files:
            with open(TRAIN_NUMBERS_PATH + file, "r", encoding="utf-8") as txt:
                for line in txt:
                    if str(train_number) in line:
                        line = file.title().split(".")
                        return line[0]


    def __parse_number(self, data):
        """
        Train number parser

        @param data:    Message content
        @return:        Train number
        """
        temp = re.search(r"Pociąg(?: nr)? (\d+)", data)

        if temp:
            return temp.group(1)
        else:
            self.status = self.status * 0

    def __parse_route(self, data):
        """
        Route parser

        @param data:    Message content
        @return:        Train route as a dictionary
        """
        x = self.data.find("relacji")  # remove beginning
        if x != -1:
            try:
                temp = self.data[x + len("relacji"):]
                temp = re.findall(r"([\w\s.]+)\s(\d{2}:\d{2})", temp)
                route = {}
                if temp:
                    route['departure_city'] = temp[0][0]
                    route['departure_time'] = temp[0][1]
                    route['arrival_city'] = temp[1][0]
                    route['arrival_time'] = temp[1][1]
                    return route
                else:
                    self.status = self.status * 0
            except IndexError:
                self.status = self.status * 0


    def __parse_type(self, data):
        """
        Type parser

        @param data:    Message content
        @return:        Message type, available:
                        - delayed
                        - cancelled
                        - not recognized
        """
        if "opóźniony" in self.data:
            return "delayed"
        elif "odwołany" in self.data:
            return "cancelled"
        else:
            self.status = self.status * 0
            return "not recognized"

    def __parse_delay(self, data):
        """
        Delay parser

        @param data:    Message content
        @return:        Train delay
        """
        temp = re.search(r"(\d+)\sminut", self.data)
        if temp:
            return temp.group(1)
        else:
            return 0  # in case of cancelled train
