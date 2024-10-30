import requests
from bs4 import BeautifulSoup
import logging


class Scrapper:
    """
    Representation of kolejeslaskie.com scrapper

    """
    def __init__(self, url):
        """
        Scrapper constructor

        @param url:     URL to information page
        """
        self.url = url

    def get_data(self):
        """
        Data getter

        @return:        List of raw messages from post titles
        """
        data = self.__download_data()
        soup = BeautifulSoup(data, 'html.parser')
        articles = soup.find_all('article', class_='post')

        titles = []

        for article in articles:
            title_link = article.find('h2').find('a')
            if title_link:
                titles.append(title_link.get_text())

        return titles

    def __download_data(self):
        """
        Download whole page

        @return:        Whole information page
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            logging.info("Page downloaded")
            return response.text
        else:
            logging.error("Connection failed: " + f'Błąd: {response.status_code}')
