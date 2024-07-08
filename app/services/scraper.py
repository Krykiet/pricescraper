import re

import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

SCRAPER_MESSAGE = 'Scraped!'

# TODO Seek for changes with every get request and scrape only when price changes

def scrape_rdn():
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        # existing headers...
    }
    url = f'https://tge.pl/energia-elektryczna-rdn?random={random.randint(10001, 99999)}'
    request = requests.get(url=url, headers=headers)
    print(f"Connected successfully + {request} {datetime.now()}")
    soup = BeautifulSoup(request.text, 'html.parser')
    # Find tables
    all_tables = soup.find_all('table')
    table = soup.select('tbody')[2]
    # All rows data
    data_table = all_tables[2]

    all_rows_data = []

    for row in table.find_all('tr'):
        row_data = []
        for td in row.find_all('td'):
            if '-' in td.text:
                row_data.append(np.nan)
            else:
                match = re.search(r"(\d+[\.,]?\d*)", td.text)
                if match:
                    row_data.append(float(match.group(1).replace(',', '.')))
        all_rows_data.append(row_data)

    return np.array(all_rows_data)


def convert_to_db_format(data_list):
    return [('NaN' if np.isnan(val) else val) for val in data_list]


class ScrapedData:

    def __init__(self):
        # Add request and bs4 data manipulation
        rdn_table = scrape_rdn()

        # HERE IS ERROR
        db_format_rdn_table = np.array([convert_to_db_format(row) for row in rdn_table])

        self.f1_price = db_format_rdn_table[:, 1]
        self.f1_volume = db_format_rdn_table[:, 2]
        self.f2_price = db_format_rdn_table[:, 3]
        self.f2_volume = db_format_rdn_table[:, 4]
        self.cont_price = db_format_rdn_table[:, 5]
        self.cont_volume = db_format_rdn_table[:, 6]
