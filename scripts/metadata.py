import logging
import os
from datetime import date

from dotenv import load_dotenv
from utils import ordinal, parse_date, save_metadata_file

load_dotenv()

logger = logging.getLogger(__name__)


def create_and_save_metadata_file(current_date: date, pinata_response: str):
    logger.info("Creating Metadata File")
    elements = parse_date(current_date)
    file_name = "-".join(elements) + ".json"

    metadata = {}

    day_of_the_month = ordinal(current_date.day)

    metadata.update(
        {
            "name": (
                f"{current_date.strftime('%B')} "
                f"{day_of_the_month}, "
                f"{current_date.strftime('%Y')}"
            ),
            "description": (
                f"NFT for the {day_of_the_month} of "
                f"{ current_date.strftime('%B %Y') } in Cistercian numerals."
            ),
            "image": f"{os.getenv('PINATA_GATEWAY')}/ipfs/{pinata_response['IpfsHash']}",
            "attributes": [
                {"trait_type": "Year", "value": current_date.strftime("%Y")},
                {"trait_type": "Month", "value": current_date.strftime("%B")},
                {"trait_type": "Day", "value": day_of_the_month},
            ],
        }
    )

    logger.info("Saving Metadata File")
    save_metadata_file(metadata, file_name)

    return file_name
