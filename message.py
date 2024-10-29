import re

LINES = {'S1': ['Gliwice', 'Katowice', 'Częstochowa'],
         'S13': ['Częstochowa', 'Lubliniec'],
         'S17': ['Gliwice', 'Rybnik'],
         'S18': ['Gliwice', 'Bytom'],
         'S3': ['Katowice', 'Kraków Główny'],
         'S31': ['Katowice', 'Mysłowice', 'Oświęcim'],
         'S4': ['Katowice', 'Tychy Lodowisko'],
         'S5': ['Katowice', 'Bielsko-Biała Główna', 'Zwardoń'],
         'S6': ['Katowice', 'Wisła Głębce'],
         'S61': ['Czechowice-Dziedzice', 'Zebrzydowice', 'Cieszyn'],
         'S62': ['Skoczów', 'Goleszów', 'Cieszyn'],
         'S7': ['Katowice', 'Rybnik', 'Racibórz'],
         'S71': ['Katowice', 'Rybnik', 'Wodzisław Śląski', 'Chałupki', 'Bohumin'],
         'S72': ['Rybnik', 'Pszczyna'],
         'S75': ['Gliwice', 'Knurów', 'Rybnik', 'Chybie', 'Bielsko-Biała', 'Żywiec'],
         'S76': ['Gliwice', 'Knurów', 'Rybnik', 'Chybie', 'Wisła Głębce'],
         'S78': ['Racibórz', 'Chałupki'],
         'S8': ['Katowice', 'Tarnowskie Góry', 'Lubliniec'],
         'S9': ['Częstochowa', 'Zawiercie', 'Pyrzowice Lotnisko', 'Tarnowskie Góry']}


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
            print("Number not found")
            self.status = self.status * 0

    def __parse_route(self, data):
        """
        Route parser

        @param data:    Message content
        @return:        Train route as a dictionary
                        departure city  :   departure time
                        arrival city    :   arrival time
        """
        x = self.data.find("relacji")  # remove beginning
        if x != -1:
            temp = self.data[x + len("relacji"):]
            temp = re.findall(r"(\w+[\s\w]*)\s(\d{2}:\d{2})", temp)

            if temp:
                route = {station: time for station, time in temp}
                return route
            else:
                print("Route not found")
                self.status = self.status * 0
        else:
            print("Route not found")
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
            print("Delay not found")
            return 0  # in case of cancelled train
