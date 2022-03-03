from bs4 import BeautifulSoup
import requests
import csv
import os

URL = 'https://krisha.kz/prodazha/kvartiry/'
headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'accept': '*/*'
    }
HOST = 'https://krisha.kz/'
FILE = 'kvartiry.csv'
def get_html(url, params=None):
    r = requests.get(url, headers=headers, params=params)
    return r

def count_of_page(html):
    soup = BeautifulSoup(html, 'lxml')
    pagenation = soup.find_all('a', class_='paginator__btn')
    if pagenation:
        return pagenation[-2].get_text(strip=True)
    else:
        return 1


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='a-card__inc')

    kvartiry = []
    for item in items:
        kvartiry.append({
                'title': item.find('div', class_='a-card__header-left').get_text(strip=True).replace('Все заметкиУдалить', ''),
                'link': HOST + item.find('a', class_='a-card__title').get('href'),
                'price': item.find('div', class_='a-card__price').get_text(strip=True).replace('\xa0', ''),
                'street': item.find('div', class_='a-card__subtitle').get_text(strip=True),
                'city': item.find('div', class_='card-stats').get_text(strip=True)

            })
    return kvartiry

def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Обьявление', 'Ссылка', 'Цена', 'Улица', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['street'], item['city']])


def parse():
    URL = input("Введите URl: ")
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        kvartira = []
        pages_count = count_of_page(html.text)
        for page in range(1, int(pages_count)):
            print(f'Парсинг страницы:{page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            kvartira.extend(get_data(html.text))
        print(len(kvartira))
        save_file(kvartira, FILE)
        os.startfile(FILE)
    else:
        print('Error')

parse()
