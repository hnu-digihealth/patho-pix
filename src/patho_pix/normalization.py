# Standard Library
import os
import tempfile

# Third Party
import requests
from histolab.stain_normalizer import (MacenkoStainNormalizer,
                                       ReinhardStainNormalizer)
from PIL import Image

# D Download link for target image
img_url = "https://user-images.githubusercontent.com/31658006/212924301-c80f454e-f99a-4479-9852-6ef988c078aa.png"

target_img = None

# Create a temporary directory to store the target image
tmp_data = tempfile.TemporaryDirectory(prefix="tmp.patho-pix.")

# Download Target image
response = requests.get(img_url)
if response.status_code == 200:
    path_img = os.path.join(tmp_data.name, "target.jpg")
    with open(path_img, "wb") as fd:
        fd.write(response.content)
        target_img = Image.open(path_img)
        target_img.save("./output/test_out/target_img.tiff")
else:
    print("Target Image could not be downloaded, please check if the link is valid.")


def normalize_tile_reinhard(tile):
    normalizer = ReinhardStainNormalizer()
    normalizer.fit(target_img)
    normalized_img = normalizer.transform(tile)
    return normalized_img


def normalize_tile_macenko(tile):
    normalizer = MacenkoStainNormalizer()
    normalizer.fit(target_img)
    normalized_img = normalizer.transform(tile)
    return normalized_img
