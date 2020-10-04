import os

import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://www.myhome.ie/pricechanges'
pages = 250


def content_to_df(text):
    soup = BeautifulSoup(text, 'lxml')

    blocks = soup.find_all('div', {"class": "PropertyPriceChangeCard__Info MhHelper__Flex--spaced"})

    l = []
    for block in blocks:
        date_str = block.find('span', {'class': 'PriceRegisterListItem__Date'}).contents[0]
        date_ = pd.to_datetime(date_str)

        change_str = block.find('span', {'class': 'mr-3'}).contents[0]
        change_str = change_str.replace('(', '').replace(')', '')
        change_str = change_str.replace('%', '')

        location = block.find('a', {'class': 'PropertyPriceChangeCard__Address'}).contents[0].split(',')[-1].strip()

        l.append({'date': date_, 'location': location, 'change': float(change_str)})

    df = pd.DataFrame(l)
    if not df.empty:
        df.set_index('date', inplace=True)
    return df


df = pd.DataFrame()
for i in range(1, pages):
    print(f'processing page {i}')
    full_url = url + f'/page-{i}'
    response = requests.get(full_url)
    df = df.append(content_to_df(response.content))

directory = dir_path = os.path.dirname(os.path.realpath(__file__))
full_file = os.path.join(directory, 'data.csv')
df.to_csv(full_file)
