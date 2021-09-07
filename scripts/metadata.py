from utils import (
  parse_date,
  save_metadata_file,
  ordinal
)

def create_and_save_metadata_file(current_date, pinata_response):
    elements = parse_date(current_date)
    file_name = '-'.join(elements) + '.json'

    metadata = {}

    day_of_the_month = ordinal(current_date.day)

    metadata.update({
      'attributes': [{
        "year": current_date.strftime('%Y'),
        "month": current_date.strftime('%B'),
        "day": day_of_the_month
      }],
      'name': f"{current_date.strftime('%B')} {day_of_the_month}, {current_date.strftime('%Y')}",
      'description': f'NFT for the {day_of_the_month} of { current_date.strftime("%B %Y") } in Cistercian numerals.',
      'image': f"https://gateway.pinata.cloud/ipfs/{pinata_response['IpfsHash']}"
    })

    save_metadata_file(metadata, file_name)

    return file_name
