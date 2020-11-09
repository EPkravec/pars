import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=java&L_save_area=true&area=1002&from=cluster_area&showClusters=true'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'accept': '*/*'}
FILE = 'hh_ru.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    vacans = []
    for item in items:
            vacans.append(
                {
                    'title': item.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get_text(strip=True),
                    'city': item.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).get_text(strip=True),
                    'price': item.find('div', class_='vacancy-serp-item__sidebar').get_text(strip=True),
                    'link_': item.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get('href'),
                }
            )
    return vacans


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='bloko-button')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1


def save_f(items, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вакансия', 'Город', 'Цена', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['city'], item['price'], item['link_']])


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        vacans = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг старницы: {page} из {pages_count}  ....')
            html = get_html(URL, params={'page': page})
            vacans.extend(get_content(html.text))
            save_f(vacans, FILE)
        print(f'Парсинг закончен всего найдено {len(vacans)} объявлений')
    else:
        print('Error: нет соединения со страницей')


parser()
