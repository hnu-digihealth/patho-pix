# import numpy as np
# import pandas as pd
# from openslide import OpenSlide as slide
# import os.path
# from pathlib import Path
# from PIL import Image

# x = pd.Series([1, 3, 5, np.nan, 6, 8])
# print(x)

# test_image_path = 'media/test-images/at3_1m4_01.tif'

# print(os.path.isfile(test_image_path))

# my_file = Path(test_image_path)
# if my_file.is_file():
#   print('is_file')
# else:
#   print('is_not_file')

# image1 = Image.open(test_image_path)
# print(image1)

# slide(test_image_path).get_thumbnail(size=(1024, 1024))


# The path can also be read from a config file, etc.
# OPENSLIDE_PATH = r'c:\path\to\openslide-win64\bin'

# import os

# print('START')

# if hasattr(os, 'add_dll_directory'):
#   # Windows
#   with os.add_dll_directory(OPENSLIDE_PATH):
#     import openslide
# else:
#   import openslide

# print('END')

# Standard Library
from io import BytesIO

# Third Party
from PIL import Image, ImageCms

test_image_path = 'media/test-images/266289986_2@small.tiff'
image = Image.open(test_image_path)
fromProfile = ImageCms.getOpenProfile(BytesIO(image.info['icc_profile']))
toProfile = ImageCms.createProfile('sRGB')
intent = ImageCms.getDefaultIntent(fromProfile)
# ImageCms.profileToProfile(
#   image, fromProfile, toProfile, intent, 'RGBA', True, 0
# )

image.show()
image.save('output/example-test/test.tiff')

print('END')
