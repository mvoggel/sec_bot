import xml.etree.ElementTree as ET
import pandas as pd
import logging
import requests

logger = logging.getLogger(__name__)

def extract_13G_data(xml_url, output_file):
    headers = {"User-Agent": "13D-Bot/1.0 (alliepetracci13@gmail.com)"}
    
    response = requests.get(xml_url, headers=headers)
    response.raise_for_status()
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()

    data = []
    for entry in root.findall(".//ownershipDocument"):
        symbol = entry.findtext("issuerName", default="Unknown")
        ownership_percentage = entry.findtext("ownershipPercentage", default="0")
        data.append({"symbol": symbol, "ownership_percentage": ownership_percentage})

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    logger.info(f"Saved 13G data to {output_file}")
