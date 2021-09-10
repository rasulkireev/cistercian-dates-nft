import os
from pathlib import Path
from datetime import date, timedelta
import time
import logging
from dotenv import load_dotenv

from image import create_and_save_image
from metadata import create_and_save_metadata_file
from utils import (
  load_file_to_Pinata,
  get_project_root,
  check_if_NFT_exists
)
from mint_nft import mintNFT

load_dotenv()
logging.basicConfig(level=logging.INFO)

def main():

    project_root = get_project_root()
    start_date = date(345,1,16)
    current_date = start_date
    end_date = date(345,1,17)

    count = 1
    while current_date <= end_date:
      startTime = time.time()

      NFT_exists = check_if_NFT_exists(current_date)
      if NFT_exists == True:
        logging.info(f"NFT for {current_date} already exists.")
        time.sleep(1.5)
      else:
        # Generate, Save and Upload Unique Date Image
        image_name = create_and_save_image(current_date)
        image_path = os.path.join(project_root, "images", image_name)
        response = load_file_to_Pinata(image_path, image_name)

        # save response hash to a txt file
        with open(f"{project_root}/pinata_hashes.txt", 'a', encoding="utf-8") as file:
          file.write("\n")
          ipfs_Hash = response['IpfsHash']
          file.write(f"{{'date': '{current_date}', 'hash': '{ipfs_Hash}', 'type': 'image'}},")

        # Generate, Save and Upload Metadata for Unique Image
        metadata_file_name = create_and_save_metadata_file(current_date, response)
        metadata_file_path = os.path.join(project_root, "metadata", metadata_file_name)
        response = load_file_to_Pinata(metadata_file_path, metadata_file_name)

        # save response hash to a txt file
        with open(f"{project_root}/pinata_hashes.txt", 'a', encoding="utf-8") as file:
          file.write("\n")
          ipfs_Hash = response['IpfsHash']
          file.write(f"{{'date': {current_date}', 'hash': '{ipfs_Hash}', 'type': 'metadata'}},")

        response = mintNFT(f"{os.getenv('PINATA_GATEWAY')}/ipfs/{response['IpfsHash']}")

        # estimating how long it will take to complete the rest
        executionTime = (time.time() - startTime)
        date_diff = (end_date - current_date).days
        time_left = (executionTime * date_diff)

        logging.info(f'NFT #{count} done ({response["transactionHash"].hex()}). {date_diff} left. Estimated time: { round(time_left / 60 / 60, 2) } hours / { round(time_left / 60, 2) } minutes / { round(time_left, 2) } seconds')

      count += 1
      current_date += timedelta(days=1)

if __name__ == "__main__":
    startTime = time.time()
    main()
    executionTime = (time.time() - startTime)

    print(f"Total time: {executionTime} seconds")