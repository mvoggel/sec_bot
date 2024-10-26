import pandas as pd
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_DEF14A_data(html_url, output_file):
    headers = {"User-Agent": "DEF14A-Bot/1.0 (alliepetracci13@gmail.com)"}
    
    response = requests.get(html_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    data = []
    for entry in soup.find_all("table"):
        rows = entry.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                data.append({"executive_name": cells[0].text.strip(), "compensation": cells[1].text.strip()})

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    logger.info(f"Saved DEF14A data to {output_file}")
