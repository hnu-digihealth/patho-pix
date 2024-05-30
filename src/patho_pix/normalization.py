import requests
import tempfile
import os
from PIL import Image

from histolab.stain_normalizer import ReinhardStainNormalizer, MacenkoStainNormalizer


img_url = "https://user-images.githubusercontent.com/31658006/212924301-c80f454e-f99a-4479-9852-6ef988c078aa.png"
test_url= 'https://user-images.githubusercontent.com/31658006/212924179-a85573b6-1bb3-4f9b-a8ab-00a26b1d652e.png'
target_img = None
test_img = None
tmp_data = tempfile.TemporaryDirectory(prefix="tmp.patho-pix.")
# Download Target image
response = requests.get(img_url)
if response.status_code == 200:
    path_img = os.path.join(tmp_data.name, "target.jpg")
    with open(path_img, "wb") as fd:
        fd.write(response.content)
        target_img = Image.open(path_img)
        target_img.save("/workspaces/patho-pix/output/test_out/target.tiff")
else:
    print("Target Image could not be downloaded")

response = requests.get(test_url)
if response.status_code == 200:
    path_img = os.path.join(tmp_data.name, "test.jpg")
    with open(path_img, "wb") as fd:
        fd.write(response.content)
        test_img=Image.open(path_img)
        test_img.save("/workspaces/patho-pix/output/test_out/test.tiff")

else: print('Test Image could not be downloaded')

def normalize_tile_reinhard(tile, dict):
    normalizer = ReinhardStainNormalizer()
    normalizer.fit(target_img)
    normalized_img = normalizer.transform(test_img)
    normalized_img.save("/workspaces/patho-pix/output/test_out/normalized.tiff")
    return normalized_img, dict


def normalize_tile_macenko(tile, dict):
    normalizer = MacenkoStainNormalizer()
    normalizer.fit(target_img)
    normalized_img = normalizer.transform(tile)
    return normalized_img, dict
