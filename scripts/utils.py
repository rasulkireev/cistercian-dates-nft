import requests
import os
from pathlib import Path
import os
import json
import random
from datetime import date
from PIL import Image, ImageOps

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def generate_random_color(date):
  random.seed(date.strftime("%Y%m%d"))
  r = lambda: random.randint(0,255)
  color = (r(),r(),r())
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
          if pixels[x,y][3] < 255:
              pixels[x,y] = (255, 255, 255)
  return image

def save_image(output_folder, file, file_name):
    project_root = get_project_root()
    file_location = f"{project_root}/{output_folder}"
    file.save(f"{file_location}/{file_name}")

def load_file_to_Pinata(file_path, file_name):
  PINATA_BASE_URL = 'https://api.pinata.cloud/'
  ENDPOINT = 'pinning/pinFileToIPFS'

  headers = {
    'pinata_api_key': os.getenv('PINATA_API_KEY'),
    'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')
  }

  with Path(file_path).open("rb") as fp:
      file_content = fp.read()
      response = requests.post(
        PINATA_BASE_URL + ENDPOINT,
        files={
          "file": (file_name, file_content)
        },
        headers=headers
      )

  return response.json()

def ordinal(n):
    if 11 <= n <= 13:
        return '{}th'.format(n)
    if n%10 == 1:
        return '{}st'.format(n)
    elif n%10 == 2:
        return '{}nd'.format(n)
    elif n%10 == 3:
        return '{}rd'.format(n)
    else:
        return '{}th'.format(n)

def save_metadata_file(metadata_dictionary, file_name):
    project_root = get_project_root()
    file_location = f"{project_root}/metadata"

    with open(f"{file_location}/{file_name}", 'a', encoding="utf-8") as file:
      json_obj = json.dumps(metadata_dictionary)
      file.write(json_obj)