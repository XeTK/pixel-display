from PIL import Image
from yaml import load

CONFIG_FILE = "config.yaml"

config_file = open(CONFIG_FILE, 'r')
config = load(config_file)

IMAGE_SIZE = config['IMAGE_SIZE']


def chunks(array, width):
    return [array[i:i + width] for i in range(0, len(array), width)]


def open_image(path):
    image = Image.open(path)

    size = IMAGE_SIZE, IMAGE_SIZE

    image.thumbnail(size)

    pixels = list(image.getdata())

    converted_pixels = []

    for pixel in pixels:
        r, g, b = pixel

        total = r
        total += (g << 8)
        total += (b << 16)

        converted_pixels.append(total)

    return chunks(converted_pixels, IMAGE_SIZE)
