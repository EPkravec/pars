# import of data exchange library
import requests
# import of a library for parsing
from bs4 import BeautifulSoup
# import of a library for working with csv files
import csv

# create constants for interacting with libraries, as well as for parsing
HOST = 'https://www.avito.ru/'  # constant for appending the host if the links in the site code are not complete
URL = 'https://www.avito.ru/izhevsk/dlya_doma_i_dachi'  # constant- the link from which to parse the information
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'accept': '*/*'}  # a constant for interaction with the site (so that the site does not think that we are a bot or
# want to do something bad)
FILE = 'avito_ru.csv'  # constant - the name of the file with the extension to which the information will be written


# create a function with parameters (link and parameters) to send get requests and return a response
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# create a function with parameters (html) to send the receipt of the necessary data from the soup object,
# through a loop and write it to the dictionary with the appropriate criteria, as well as return the recorded
# data in the dictionary
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item__line')
    tovar = []

    for item in items:
        tovar.append(
            {
                'title': item.find('span', class_='snippet-link-name').get_text(strip=True),
                'link_': HOST + item.find('a', class_='snippet-link').get('href'),
                'price': item.find('span', class_='snippet-price').get_text(strip=True),
                'type': item.find('span', class_='snippet-text').get_text(strip=True)
            }
        )
    return tovar


# create a function with parameters (html) to determine the number of pages on the specified link with products
# and return if there are pages, return their number, otherwise return only 1
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1


# create a function with parameters (items end path) for writing and editing the received data with headers
# (product name, price, etc.) in the csv file, as well as assigning the headers to the headers by iterating through
# the cycle of the corresponding data from the item dictionary
def save_f(items, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название товара', 'Цена товара', 'Категория'], 'Ссылка на товар')
        for item in items:
            writer.writerow([item['title'], item['price'], item['type'], item['link_']])


# create a parser function with conditions,
# if we get a response of 200 with the html variable, then we create a tovar list, get a variable with the
# number of pages pages_count, in a loop we go through the parameter P (a variable on each new page) with a step from
# 1 to pages_count +1 pages. the received data is added to the tovar dictionary and copied to the file. If the response
# from html is not 200, we display a message that an error has occurred
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
        print(f'Парсинг закончен всего найдено {len(tovar)} объявлений')
    else:
        print('Error: нет соединения со страницей')


parser()
