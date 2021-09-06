import os
from pathlib import Path
from datetime import date, timedelta
import time

from generate_image import (
  generate_random_color,
  parse_date,
  get_number_decomposition,
  number_string_2_integers,
  composer_numeral_image,
  transparent_to_opaque_bg,
  compose_final_image,
  save_image
)

def main():

    start_date = date(1,1,1)
    end_date = date(2100,1,1)

    current_date = start_date

    count = 0
    while current_date <= end_date:
      elements = parse_date(current_date)
      images = []
      for element in elements:
        decomposition = get_number_decomposition(element)
        result = composer_numeral_image(number_string_2_integers(decomposition))
        images.append(result)
      color = generate_random_color(current_date)
      result = compose_final_image(images, color)
      save_image(result, '-'.join(elements))
      count += 1
      print(f'Generated image #{count}')

      current_date += timedelta(days=1)

if __name__ == "__main__":
    # run the main script from its owb directory
    script_location = Path(__file__).absolute().parent
    os.chdir(script_location)

    startTime = time.time()
    main()
    executionTime = (time.time() - startTime)