import requests
from bs4 import BeautifulSoup
import numpy as np
import re

SCRAPER_MESSAGE = 'Scraped!'

res = requests.get('https://tge.pl/energia-elektryczna-rdn')

print(f"Connected successfully + {res}")

soup = BeautifulSoup(res.text, 'html.parser')
table = soup.select('tbody')[2]
all_rows = table.select('.footable-visible')

f1_nums = np.arange(1, len(all_rows), 7)
f2_nums = np.arange(3, len(all_rows), 7)
np_rows = np.array(all_rows, dtype=object)
# Fixing 1
f1_rows = np_rows[f1_nums]
f2_rows = np_rows[f2_nums]


def get_price_from_div(div_item):
    str_price = re.sub('[^0-9.]', '', div_item.text)
    return str_price


def extract_prices(div_item):
    prices = []
    for row in div_item:
        price = get_price_from_div(row)

        price_float = price[:-2] + '.' + price[-2:]

        prices.append(float(price_float))

    return prices


f1_prices = extract_prices(f1_rows)
f2_prices = extract_prices(f2_rows)


def get_prices():
    """
    Returns tuple of prices (fixing_I, fixing_II)

    :return:
    """
    return f1_prices, f2_prices
