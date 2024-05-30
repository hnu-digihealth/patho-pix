# Third Party
from PIL import Image


def convert_jpeg_to_tiff(image_path, output_path):
    im = Image.open(image_path)
    im.save(output_path, 'TIFF')
