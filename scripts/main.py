import json
import logging.config
import os
import time
from datetime import date, timedelta

from dotenv import load_dotenv
from image import create_and_save_image
from mint_nft import mintNFT
from settings import LOGGING_CONFIG
from utils import check_if_NFT_exists, get_project_root, load_file_to_Pinata

from metadata import create_and_save_metadata_file

load_dotenv()

logger = logging.getLogger(__name__)


def main():

    project_root = get_project_root()
    start_date = date(1541, 3, 15)
    current_date = start_date
    end_date = date(1541, 3, 15)

    count = 1
    while current_date <= end_date:
        logging.info(f"Creating and Minting {current_date} NFT")
        startTime = time.time()

        NFT_exists = check_if_NFT_exists(current_date)
        if NFT_exists == True:
            logger.info(f"{current_date} NFT exists.")
            time.sleep(1.5)
        else:
            # Generate, Save and Upload Unique Date Image
            image_name = create_and_save_image(current_date)
            image_path = os.path.join(project_root, "images", image_name)
            image_response = load_file_to_Pinata(image_path, image_name)

            # Generate, Save and Upload Metadata for Unique Image
            metadata_file_name = create_and_save_metadata_file(
                current_date, image_response
            )
            metadata_file_path = os.path.join(
                project_root, "metadata", metadata_file_name
            )
            metadata_response = load_file_to_Pinata(
                metadata_file_path, metadata_file_name
            )

            # Mint the NFT
            minting_tx, minting_response = mintNFT(
                f"{os.getenv('PINATA_GATEWAY')}/ipfs/{metadata_response['IpfsHash']}"
            )

            # estimating how long it will take to complete the rest
            execution_time = time.time() - startTime
            date_diff = (end_date - current_date).days
            time_left = execution_time * date_diff

            logger.info(
                (
                    f"{current_date} NFT is done. "
                    f"{date_diff} left. Estimated time: "
                    f"{ round(time_left / 60 / 60, 2) } hours"
                )
            )

            with open(
                f"{project_root}/tracking-{os.getenv('ENV')}.json",
                "a+",
                encoding="utf-8",
            ) as file:
                file.write("\n")
                file.write(
                    (
                        "{\n"
                        f'  "date": "{current_date}",\n'
                        f'  "mint_duration": {execution_time},\n'
                        f'  "metadata_pinata_hash": "{metadata_response["IpfsHash"]}",\n'
                        f'  "image_pinata_hash": "{image_response["IpfsHash"]}",\n'
                        f'  "transaction_hash": "{minting_response["transactionHash"].hex()}",\n'
                        f'  "minting_transaction_details": {json.dumps(minting_tx)}\n'
                        "},"
                    )
                )

        count += 1
        current_date += timedelta(days=1)


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)
    startTime = time.time()
    main()
    executionTime = time.time() - startTime
