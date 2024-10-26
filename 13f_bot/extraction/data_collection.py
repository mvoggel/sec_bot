import logging
import requests
import pandas as pd
from datetime import datetime
import sys
import os

# Add project root directory to the module search path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Now you can import from main.config
import main.config as config
import extraction.parse_extract as parse_extract  # Adjust based on your structure

logger = logging.getLogger(__name__)

def fetch_and_extract_filings(cik, form_types):
    base_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {"User-Agent": "13F-Bot/1.0 (alliepetracci13@gmail.com)"}
    try:
        logger.info(f"Fetching filings for CIK: {cik}")
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()

        filings_data = response.json()
        filings_list = filings_data.get('filings', {}).get('recent', {})
        form_list = filings_list.get('form', [])
        accession_numbers = filings_list.get('accessionNumber', [])
        primary_documents = filings_list.get('primaryDocument', [])

        if not form_list or not accession_numbers or not primary_documents:
            logger.error("No recent filings data found in the response.")
            return

        # Track missing forms
        found_form_types = set()

        # Process each form based on form type
        for i, form_type in enumerate(form_list):
            if form_type in form_types:
                found_form_types.add(form_type)  # Track found types
                accession_number = accession_numbers[i].replace("-", "")
                document_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_documents[i]}"
                
                # Define unique output file paths for each form type
                output_file = f"data/{form_type.replace(' ', '_')}_data.csv"
                logger.info(f"Processing {form_type} filing at {document_url}")
                
                parse_extract.parse_and_extract(form_type, document_url, output_file)
            else:
                logger.warning(f"Skipping non-matching form: {form_type}")

        # Log missing forms that were not detected in recent filings
        missing_form_types = set(form_types) - found_form_types
        if missing_form_types:
            logger.warning(f"Missing form types for CIK {cik}: {', '.join(missing_form_types)}")

    except requests.RequestException as e:
        logger.error(f"Error fetching filings from SEC EDGAR API: {e}")


if __name__ == "__main__":
    cik = "0001067983"  # Example CIK for Berkshire Hathaway
    form_types = ["13F-HR", "13D", "13G", "4", "10-Q", "10-K", "DEF 14A", "S-1"]
    fetch_and_extract_filings(cik, form_types)
    logger.info("Data collection and extraction process completed.")
