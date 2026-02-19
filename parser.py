import requests
from bs4 import BeautifulSoup
import csv
import json

class EstateParser:
    def __init__(self, target_url):
        self.url = target_url
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch_data(self):
        # здесь будет логика пагинации
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        return None

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        listings = []
        # Пример логики поиска (селекторы зависят от сайта)
        for item in soup.select('.listing-item'):
            title = item.select_one('.title').text.strip()
            price = item.select_one('.price').text.strip()
            listings.append({
                'title': title,
                'price': price
            })
        return listings

    def save_to_csv(self, data, filename='market_data.csv'):
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

if __name__ == "__main__":
    print("Starting Scraper...")
