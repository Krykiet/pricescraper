import re
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import numpy as np

def scrape_block_contracts_table():
    """
    Fetch data from the specified block contracts table and extract the contract name, min price, max price, and volume.
    :param table_id: The ID of the table to scrape (e.g., 'footable_kontrakty_blokowe_0').
    """
    url = "https://www.tge.pl/energia-elektryczna-rdn"
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }

    request = requests.get(url, headers=headers)
    print(f"Connected successfully to block contracts table + {request} {datetime.now()}")
    soup = BeautifulSoup(request.text, 'html.parser')

    # Locate the table by its unique ID
    table = soup.find('table', {'id': 'footable_kontrakty_blokowe_0'})
    if not table:
        raise ValueError(f"Table with ID {'footable_kontrakty_blokowe_0'} not found on the page.")

    # Extract data from table rows
    block_contracts_data = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')

        if len(cells) < 4:
            continue  # Skip rows without enough data

        def parse_cell(cell):
            value = cell.text.strip()
            return float(value.replace(',', '.')) if value != '-' and value else None

        contract_data = {
            'contract_name': cells[0].text.strip(),  # First column: Contract name
            'min_price': parse_cell(cells[1]),  # Min price
            'max_price': parse_cell(cells[2]),  # Max price
            'volume': parse_cell(cells[3])  # Volume
        }

        block_contracts_data.append(contract_data)

    return block_contracts_data

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

class BlockContractsScraper:

    def __init__(self):
        # Scrape data from the block contracts table
        block_contracts_data = scrape_block_contracts_table()

        # Convert to database-compatible format
        db_format_block_contracts = convert_to_db_format(block_contracts_data)

        self.block_contracts = db_format_block_contracts