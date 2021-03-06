import logging
import os

from PIL import Image, ImageOps
from utils import (
    get_project_root,
    parse_date,
    save_image,
    transparent_to_opaque_bg,
)

logger = logging.getLogger(__name__)


def get_number_decomposition(number_string):
    """Decomposes the number in its digits.
    Returns a list of strings [units, tens, hundreds, thousands].
    """
    number = int(number_string)

    decomposition = [number_string[len(number_string) - 1]]

    for i in range(1, 4):
        if number >= pow(10, i):
            decomposition.append(number_string[len(number_string) - (i + 1)])
    return decomposition


def number_string_2_integers(_list):
    """Gets a list of strings and returns a list of the correspondant integers.
    Returns the translated list.
    """
    integer_list = []
    for _int_str in _list:
        integer_list.append(int(_int_str))
    return integer_list


def composer_numeral_image(decomposition):
    project_root = get_project_root()
    digit0 = os.path.join(project_root, "scripts", "img", "digit0.png")

    out = Image.open(digit0).convert("RGBA")
    units_images = []

    for i in range(1, 10):
        digit_1_to_10 = os.path.join(
            project_root, "scripts", "img", f"digit{i}.png"
        )
        units_images.append(Image.open(digit_1_to_10).convert("RGBA"))

    position = 0
    for element in decomposition:
        if element > 0:
            digit_image = units_images[(decomposition[position]) - 1]
            if position == 1:
                digit_image = ImageOps.mirror(digit_image)
            elif position == 2:
                digit_image = ImageOps.flip(digit_image)
            elif position == 3:
                digit_image = ImageOps.mirror(ImageOps.flip(digit_image))
            out = Image.alpha_composite(out, digit_image)
        position += 1

    return out


def compose_final_image(images):
    space_between_images = 50
    width = (space_between_images * 2) + (186 * 3)
    height = 266

    canvas = Image.new("RGBA", (width, height), color=(255, 255, 255, 0))
    for count, image in enumerate(images):
        image = transparent_to_opaque_bg(image)
        image_width, image_height = image.size
        image = image.resize((image_width * 2, image_height * 2))
        image_width, image_height = image.size

        pastex = int(image_width * count) + (space_between_images * count)
        pastey = 0

        canvas.paste(image, box=(pastex, pastey), mask=0)

    return canvas


def create_and_save_image(current_date):
    elements = parse_date(current_date)
    image_name = "-".join(elements) + ".png"

    images = []
    for element in elements:
        decomposition = get_number_decomposition(element)
        result = composer_numeral_image(
            number_string_2_integers(decomposition)
        )
        images.append(result)

    logger.info("Creating Image")
    final_image = compose_final_image(images)

    logger.info("Saving Image")
    save_image("images", final_image, image_name)

    return image_name
