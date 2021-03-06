import json
import os
import random
import time
from datetime import date
from pathlib import Path

import requests

PINATA_BASE_URL = "https://api.pinata.cloud/"


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def generate_random_color(date):
    random.seed(date.strftime("%Y%m%d"))
    r = lambda: random.randint(0, 255)
    color = (r(), r(), r())
    return color


def parse_date(date: date):
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)

    return [year, month, day]


def transparent_to_opaque_bg(image):
    pixels = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if pixels[x, y][3] < 255:
                pixels[x, y] = (255, 255, 255, 0)
    return image


def save_image(output_folder, file, file_name):
    project_root = get_project_root()
    file_location = f"{project_root}/{output_folder}"
    file.save(f"{file_location}/{file_name}")


def load_file_to_Pinata(file_path, file_name):
    ENDPOINT = "pinning/pinFileToIPFS"

    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    with Path(file_path).open("rb") as fp:
        file_content = fp.read()
        response = requests.post(
            PINATA_BASE_URL + ENDPOINT,
            files={"file": (file_name, file_content)},
            headers=headers,
        )

    return response.json()


def ordinal(n):
    if 11 <= n <= 13:
        return f"{n}th"
    if n % 10 == 1:
        return f"{n}st"
    if n % 10 == 2:
        return f"{n}nd"
    if n % 10 == 3:
        return f"{n}rd"
    return f"{n}th"


def save_metadata_file(metadata_dictionary, file_name):
    project_root = get_project_root()
    file_location = f"{project_root}/metadata"

    with open(f"{file_location}/{file_name}", "a", encoding="utf-8") as file:
        json_obj = json.dumps(metadata_dictionary)
        file.write(json_obj)


def list_Pinata_files():
    ENDPOINT = "data/pinList?pageLimit=1000&status=pinned"

    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    response = requests.get(PINATA_BASE_URL + ENDPOINT, headers=headers)

    return response.json()


def remove_all_files_from_Pinata():

    ENDPOINT = "pinning/unpin/"

    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    files = list_Pinata_files()

    for file in files["rows"]:
        response = requests.delete(
            PINATA_BASE_URL + ENDPOINT + file["ipfs_pin_hash"], headers=headers
        )
        time.sleep(0.75)
        print(response.json)


def check_if_NFT_exists(current_date):
    elements = parse_date(current_date)
    image_name = "-".join(elements) + ".png"
    ENDPOINT = f"data/pinList?status=pinned&metadata[name]={image_name}"

    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    response = requests.get(PINATA_BASE_URL + ENDPOINT, headers=headers).json()

    try:
        if response["count"] > 0:
            rows = response["rows"]
            image_names = []
            for row in rows:
                image_names.append(row["metadata"]["name"])
            return image_name in image_names
        return False
    except KeyError:
        return response
