import pandas as pd
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def extract_10K_data(html_url, output_file):
    headers = {"User-Agent": "10K-Bot/1.0 (alliepetracci13@gmail.com)"}
    
    response = requests.get(html_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    data = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                data.append({"year": cells[0].text.strip(), "net_income": cells[1].text.strip()})

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    logger.info(f"Saved 10K data to {output_file}")
