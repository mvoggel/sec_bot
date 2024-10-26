import logging
import os
from extraction.data_collection import download_filings
from extraction.parse_extract import extract_data

logging.basicConfig(
    filename='logs/13f_bot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    investor_cik = "0001067983"  # Example CIK for Berkshire Hathaway
    form_types = ["13F-HR", "13D", "13G", "4", "10-Q", "DEF 14A", "S-1"]

    logger.info("Starting data collection for filings.")
    filings = download_filings(investor_cik, form_types)
    
    if filings.empty:
        logger.error("No filings found. Exiting.")
        return

    logger.info(f"Found {len(filings)} filings. Starting data extraction.")
    
    # Create directories if needed
    output_dir = "data/extracted_data"
    os.makedirs(output_dir, exist_ok=True)

    # Extract data for each filing
    for _, row in filings.iterrows():
        form_type = row['form_type']
        url = row['url']
        extracted_data = extract_data(form_type, url)
        if extracted_data:
            # Save the extracted data to a CSV
            output_file = os.path.join(output_dir, f"{form_type}_{row['symbol']}.csv")
            with open(output_file, 'w') as f:
                # This is just a sample way to save it, modify based on structure
                for data in extracted_data:
                    f.write(",".join(str(item) for item in data) + "\n")

    logger.info("Data extraction complete.")

if __name__ == "__main__":
    main()
