import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

class OlxParser:
    def __init__(self):
        self.url = "https://www.olx.uz/d/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
        self.data = []

    def get_html(self, page=1):
        params = {'page': page} if page > 1 else {}
        try:
            # Делаем вид, что мы обычный браузер
            res = requests.get(self.url, headers=self.headers, params=params, timeout=15)
            res.raise_for_status()
            return res.text
        except Exception as e:
            print(f"Ошибка при загрузке страницы {page}: {e}")
            return None

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # Ищем контейнеры объявлений (селекторы на OLX могут меняться, это типичные для 2024-2025)
        offers = soup.select('div[data-cy="l-card"]')
        
        for offer in offers:
            try:
                title = offer.select_one('h6').get_text(strip=True)
                # Цена на OLX часто в разных форматах (у.е. или сум)
                price_raw = offer.select_one('p[data-testid="ad-price"]').get_text(strip=True)
                link = "https://www.olx.uz" + offer.select_one('a')['href']
                location = offer.select_one('p[data-testid="location-date"]').get_text(strip=True)

                self.data.append({
                    'title': title,
                    'price': price_raw,
                    'location': location.split(' - ')[0], # Берем только город/район
                    'link': link
                })
            except (AttributeError, TypeError):
                continue

    def save(self):
        if not self.data:
            print("Данные не собраны.")
            return
        
        df = pd.DataFrame(self.data)
        # Сохраняем в CSV, который легко открывается в Excel
        df.to_csv('olx_apartments.csv', index=False, encoding='utf-8-sig')
        print(f"Готово! Сохранено {len(self.data)} объявлений.")

if __name__ == "__main__":
    bot = OlxParser()
    print("Начинаю парсинг OLX.uz...")
    
    # Парсим первые 2 страницы для примера
    for p in range(1, 3):
        html = bot.get_html(p)
        if html:
            bot.parse(html)
            print(f"Страница {p} обработана")
            time.sleep(random.uniform(2, 5)) # Важно, чтобы OLX не забанил по IP
    
    bot.save()
