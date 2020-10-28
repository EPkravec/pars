import requests.models
from bs4 import BeautifulSoup
import csv

HOST = 'https://www.avito.ru/'
URL = 'https://www.avito.ru/izhevsk/dlya_doma_i_dachi'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'accept': '*/*'}
FILE = 'parse_avito.csv'


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item__line')
    tovar = []

    for item in items:
        tovar.append(
            {
                'title': item.find('span', class_='snippet-link-name').get_text(strip=True),
                'link_': HOST + item.find('a', class_='snippet-link').get('href'),
                'price': item.find('span', class_='snippet-price').get_text(strip=True)
            }
        )
    return tovar

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1

def save_f(items, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название товара', 'Ссылка на товар', 'Цена товара'])
        for item in items:
            writer.writerow([item['title'], item['link_'], item['price']])


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        tovar = []
        pages_count = get_pages_count(html.text)
        for p in range(1, pages_count + 1):
            print(f'Парсинг старницы: {p} из {pages_count}  ....')
            html = get_html(URL, params={'p': p})
            tovar.extend(get_content(html.text))
            save_f(tovar, FILE)
        print('Парсинг закончен')
    else:
        print('Error: нет соединения со страницей')


parser()
