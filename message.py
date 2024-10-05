import re


class Message:
    def __init__(self, data):
        self.data = data
        self.status = 1         # 1 - message correct, 0 - message incorrect
        self.sent = 0

        self.type = self.__parse_type(data)

        if self.type == "delayed" or "canceled":
            self.number = self.__parse_number(data)
            self.route = self.__parse_route(data)
            self.delay = self.__parse_delay(data)

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.data == other.data
        return False

    def __hash__(self):
        return hash(self.data)

    def get_status(self):
        return self.status

    def get_type(self):
        return self.type

    def get_number(self):
        return self.number

    def get_route(self):
        return self.route

    def get_delay(self):
        return self.delay

    def get_data(self):
        return self.data

    def is_sent(self):
        return self.sent

    def send(self):
        self.sent = 1

    def __parse_number(self, data):
        temp = re.search(r"Pociąg nr (\d+)", self.data)

        if temp:
            return temp.group(1)
        else:
            print("Number not found")
            self.status = self.status * 0

    def __parse_route(self, data):

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
        if "opóźniony" in self.data:
            return "delayed"
        elif "odwołany" in self.data:
            return "cancelled"
        else:
            self.status = self.status * 0
            return "not recognized"

    def __parse_delay(self, data):
        temp = re.search(r"(\d+)\sminut", self.data)
        if temp:
            return temp.group(1)
        else:
            print("Delay not found")
            return 0                    # in case of cancelled train
