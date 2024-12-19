"""
TGeBase i średnioważone ceny godzinowe
URL:
https://www.tge.pl/energia-elektryczna-rdn-tge-base?date_start=2024-12-04&iframe=1
"""
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import numpy as np

def get_delivery_date():
    """
    Fetch the delivery date from the Indeksy page by searching for the string 'dla dostawy w dniu'.
    """
    url = "https://www.tge.pl/energia-elektryczna-rdn"
    request = requests.get(url)
    print(f"Connected successfully to Indeksy + {request} {datetime.now()}")
    soup = BeautifulSoup(request.text, 'html.parser')

    # Search for the text 'dla dostawy w dniu'
    full_text = soup.get_text()
    delivery_date_match = re.search(r"dla dostawy w dniu (\d{2}-\d{2}-\d{4})", full_text)
    if delivery_date_match:
        return datetime.strptime(delivery_date_match.group(1), "%d-%m-%Y")

    raise ValueError("Delivery date not found on the Indeksy page.")


def scrape_wahp():
    """
    Fetch the data from the wahp table and combine it with the delivery date.
    """
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }
    url = 'https://tge.pl/energia-elektryczna-rdn-tge-base?date_start=2024-12-18&iframe=1'
    request = requests.get(url=url, headers=headers)
    print(f"Connected successfully to wahp + {request} {datetime.now()}")
    soup = BeautifulSoup(request.text, 'html.parser')

    # Fetch the delivery date from the Indeksy page
    delivery_date = get_delivery_date()

    # Find the table using its ID
    table = soup.find('table', {'id': 'footable_kontrakty_godzinowe'})
    if not table:
        raise ValueError("Table not found on the wahp page.")

    # Extract data from the table rows
    all_rows_data = []
    for row in table.find('tbody').find_all('tr'):
        row_data = {}
        cells = row.find_all('td')

        # Combine delivery date with time range to form datetime
        time_range = cells[0].text.strip()  # First column (e.g., "0-1")
        start_hour, _ = map(int, time_range.split('-'))
        datetime_value = delivery_date + timedelta(hours=start_hour)
        row_data['datetime'] = datetime_value

        # Extract the other columns
        row_data['price_pln_mwh'] = float(
            cells[1].text.strip().replace(',', '.')) if cells[1].text.strip() else None
        row_data['volume_mwh'] = float(
            cells[2].text.strip().replace(',', '.')) if cells[2].text.strip() else None

        all_rows_data.append(row_data)

    return all_rows_data

def convert_to_db_format(data_list):
    return [('NaN' if np.isnan(val) else val) for val in data_list]


class ScrapedDataBase:

    def __init__(self):
        # Scrape data from the new table
        rdn_base_table = scrape_wahp()

        # Convert to database-compatible format
        db_format_rdn_base_table = np.array([convert_to_db_format(row) for row in rdn_base_table])

        self.time_periods = db_format_rdn_base_table[:, 0]
        self.prices = db_format_rdn_base_table[:, 1]
        self.volumes = db_format_rdn_base_table[:, 2]