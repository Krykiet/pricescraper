import re
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import numpy as np


def scrape_indices_table(table_id):
    """
    Fetch data from the specified wyniki-table-indeksy table and extract the index name, price, and volume.
    :param table_id: The ID of the table to scrape (e.g., 'footable_indeksy_0', 'footable_indeksy_1').
    """
    url = "https://www.tge.pl/energia-elektryczna-rdn"
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }

    request = requests.get(url, headers=headers)
    print(f"Connected successfully to wyniki-table-indeksy + {request} {datetime.now()}")
    soup = BeautifulSoup(request.text, 'html.parser')

    # Locate the table by its unique ID
    table = soup.find('table', {'id': table_id})
    if not table:
        raise ValueError(f"Table with ID {table_id} not found on the page.")

    # Extract data from table rows
    indices_data = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')

        if len(cells) < 5:
            continue  # Skip rows without enough data

        index_data = {
            'index_name': cells[0].text.strip(),  # First column: Index name
            'price_pln_mwh': float(cells[2].text.strip().replace(',', '.')) if cells[2].text.strip() else None,
            'volume_mwh': float(cells[4].text.strip().replace(',', '.')) if cells[4].text.strip() else None
        }

        indices_data.append(index_data)

    return indices_data


def convert_to_db_format(data_list):
    """
    Convert list data to a format compatible with database operations.
    """
    return [
        {
            key: ('NaN' if np.isnan(val) else val) if isinstance(val, float) else val
            for key, val in data.items()
        }
        for data in data_list
    ]


class ExtendedScrapedData:

    def __init__(self):
        # Scrape data from both tables
        indices_table_0_data = scrape_indices_table('footable_indeksy_0')
        indices_table_1_data = scrape_indices_table('footable_indeksy_1')

        # Combine data from both tables
        all_indices_data = indices_table_0_data + indices_table_1_data

        # Convert to database-compatible format
        db_format_indices_table = convert_to_db_format(all_indices_data)

        self.indices = db_format_indices_table
