import os
import random
from datetime import date
from PIL import Image, ImageOps


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
    out = Image.open('img/digit0.png').convert('RGBA')
    units_images = []

    for i in range(1, 10):
        filename = "img/digit{}.png".format(i)
        units_images.append(Image.open(filename).convert('RGBA'))

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

def transparent_to_opaque_bg(image, color):
  pixels = image.load()
  for y in range(image.size[1]):
      for x in range(image.size[0]):
          if pixels[x,y][3] < 255:
              # pixels[x,y] = color
              pixels[x,y] = (255, 255, 255)
  return image

def compose_final_image(images, color):
  width, height = 750, 500

  # canvas = Image.new("RGBA", (width, height), color = color)
  canvas = Image.new("RGBA", (width, height), color = (255, 255, 255))
  for count, image in enumerate(images):
    image = transparent_to_opaque_bg(image, color)
    image_width, image_height = image.size
    image = image.resize((image_width*2,image_height*2))
    image_width, image_height = image.size

    if count == 0:
      pastex = int(width/3 * count) + 65
      pastey = int(height / 2) - int(image_height/2)
    else:
      pastex = int(width/3 * count)
      pastey = int(height / 2) - int(image_height/2)

    canvas.paste(image, box = (pastex, pastey), mask=0)

  return canvas

def save_image(image, name):
    output_folder_name = "../images"
    if not os.path.exists(output_folder_name):
        os.mkdir(output_folder_name)
    image.save("{}/{}.png".format(output_folder_name, name))