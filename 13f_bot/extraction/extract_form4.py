import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd

logger = logging.getLogger(__name__)

def extract_form4_data(url, output_file):
    """
    Extracts data from an SEC Form 4 HTML page and writes it to a CSV file.
    """
    headers = {
        "User-Agent": "13F-Bot/1.0 (alliepetracci13@gmail.com)"
    }

    try:
        # Download the HTML content
        logger.info(f"Downloading Form 4 document from {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'lxml')

        # Extract Table I (Non-Derivative Securities)
        table_1 = soup.find('table', text="Table I - Non-Derivative Securities Acquired, Disposed of, or Beneficially Owned")
        table_1_data = extract_table_data(table_1)

        # Extract Table II (Derivative Securities)
        table_2 = soup.find('table', text="Table II - Derivative Securities Acquired, Disposed of, or Beneficially Owned")
        table_2_data = extract_table_data(table_2)

        # Combine data from both tables
        all_data = table_1_data + table_2_data

        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(all_data)
        df.to_csv(output_file, index=False)

        logger.info(f"Extracted {len(df)} entries from Form 4 and saved to {output_file}")

    except Exception as e:
        logger.error(f"Error extracting data from Form 4 at {url}: {e}")


def extract_table_data(table):
    """
    Extracts rows of data from a given HTML table.
    """
    if not table:
        return []

    data = []
    rows = table.find_all('tr')[2:]  # Skip the header rows
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 7:  # Ensure the row has enough columns
            entry = {
                'Title of Security': cols[0].text.strip(),
                'Transaction Date': cols[1].text.strip(),
                'Transaction Code': cols[4].text.strip(),
                'Amount': cols[5].text.strip(),
                'Price': cols[6].text.strip(),
            }
            data.append(entry)
    return data
