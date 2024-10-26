import logging
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_13F_data(url, output_file):
    """
    Downloads and extracts data from a 13F-HR filing.
    """
    headers = {"User-Agent": "13F-Bot/1.0 (alliepetracci13@gmail.com)"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Attempt XML parsing
        try:
            root = ET.fromstring(response.content)
            stock_data = []
            for info_table in root.findall(".//infoTable"):
                stock_data.append({
                    'symbol': info_table.findtext('nameOfIssuer', default="Unknown"),
                    'allocation': info_table.findtext('value', default=0)
                })
            
            # Save to CSV if XML parsing is successful
            if stock_data:
                df = pd.DataFrame(stock_data)
                df.to_csv(output_file, mode='a', header=False, index=False)
                logger.info(f"Saved {len(df)} entries for 13F-HR to {output_file}")
                return
            else:
                logger.warning(f"No entries parsed from 13F-HR at {url}")

        except ET.ParseError:
            # XML parsing failed, use HTML fallback
            logger.warning(f"XML parsing failed for 13F-HR at {url}. Falling back to HTML parsing.")
            soup = BeautifulSoup(response.content, 'html.parser')
            stock_data = []

            for row in soup.find_all("infoTable"):
                issuer = row.find("nameOfIssuer")
                value = row.find("value")
                stock_data.append({
                    'symbol': issuer.get_text(strip=True) if issuer else "Unknown",
                    'allocation': value.get_text(strip=True) if value else 0
                })

            if stock_data:
                df = pd.DataFrame(stock_data)
                df.to_csv(output_file, mode='a', header=False, index=False)
                logger.info(f"Saved {len(df)} entries for 13F-HR (HTML fallback) to {output_file}")
            else:
                logger.warning(f"No entries parsed from 13F-HR HTML fallback at {url}")

    except Exception as e:
        logger.error(f"Error extracting 13F data from {url}: {e}")
