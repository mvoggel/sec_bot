import logging
from .extract_10Q import extract_10Q_data
from .extract_10K import extract_10K_data
from .extract_13F import extract_13F_data
from .extract_13D import extract_13D_data
from .extract_13G import extract_13G_data
from .extract_DEF14A import extract_DEF14A_data
from .extract_form4 import extract_form4_data
from .extract_s1 import extract_s1_data

logger = logging.getLogger(__name__)

def parse_and_extract(form_type, url, output_file):
    """
    Routes the form URL to the appropriate extraction function based on form type.
    """
    try:
        if form_type == "10-Q":
            logger.info(f"Extracting 10-Q data from {url}")
            extract_10Q_data(url, output_file)
        elif form_type == "10-K":
            logger.info(f"Extracting 10-K data from {url}")
            extract_10K_data(url, output_file)
        elif form_type == "13F-HR":
            logger.info(f"Extracting 13F-HR data from {url}")
            extract_13F_data(url, output_file)
        elif form_type == "13D":
            logger.info(f"Extracting 13D data from {url}")
            extract_13D_data(url, output_file)
        elif form_type == "13G":
            logger.info(f"Extracting 13G data from {url}")
            extract_13G_data(url, output_file)
        elif form_type == "DEF 14A":
            logger.info(f"Extracting DEF 14A data from {url}")
            extract_DEF14A_data(url, output_file)
        elif form_type == "4":
            logger.info(f"Extracting Form 4 data from {url}")
            extract_form4_data(url, output_file)
        elif form_type == "S-1":
            logger.info(f"Extracting S-1 data from {url}")
            extract_s1_data(url, output_file)
        else:
            logger.warning(f"Form type {form_type} is not supported for extraction.")
    except Exception as e:
        logger.error(f"Error extracting data from {form_type} at {url}: {e}")
