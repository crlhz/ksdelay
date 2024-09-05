import requests
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, url):
        self.url = url

    def get_data(self):
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
        response = requests.get(self.url)

        if response.status_code == 200:
            return response.text
        else:
            print(f'Błąd: {response.status_code}')
