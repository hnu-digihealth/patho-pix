# Standard Library
import os
import tempfile
import unittest

# Third Party
import requests
from PIL import Image

# patho_pix
from patho_pix.normalization import (normalize_tile_macenko,
                                     normalize_tile_reinhard)

test_img_url = 'https://user-images.githubusercontent.com/31658006/212924179-a85573b6-1bb3-4f9b-a8ab-00a26b1d652e.png'


class NormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_img = None
        # Create temporary directory for dummy data
        tmp_data = tempfile.TemporaryDirectory(prefix="tmp.patho-pix.")
        # Load test image
        response = requests.get(test_img_url)
        if response.status_code == 200:
            path_img = os.path.join(tmp_data.name, "test.jpg")
            with open(path_img, "wb") as fd:
                fd.write(response.content)
                self.test_img = Image.open(path_img)
                self.test_img.save("./output/test_out/test_img.tiff")

    def test_normalize_tile_reinhard(self):
        # Test Reinhard stain normalization
        self.normalized_tile = normalize_tile_reinhard(self.test_img)
        print(type(self.normalized_tile))
        self.assertIsInstance(self.normalized_tile, Image.Image)
        # Save image in output/test_out for inspection
        self.normalized_tile.save("./output/test_out/normalized_tile_reinhard.tiff")

    def test_normalize_tile_macenko(self):
        # Test Macenko stain normalization
        self.normalized_tile = normalize_tile_macenko(self.test_img)
        self.assertIsInstance(self.normalized_tile, Image.Image)
        # Save image in output/test_out for inspection
        self.normalized_tile.save("./output/test_out/normalized_tile_macenko.tiff")
