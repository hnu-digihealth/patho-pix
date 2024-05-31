# =========================================================== #
#  Author:       Hackathon UKSH Team 14 - Patho-Pix           #
#  Copyright:    Patho-Pix Team - 2024                        #
# =========================================================== #
# -----------------------------------------------------#
#                   Library imports                    #
# -----------------------------------------------------#
# External libraries
# Standard Library
import os
import tempfile
import unittest

# Third Party
import requests

# patho_pix
# Internal libraries
from patho_pix.io import load_mask, load_wsi
from patho_pix.tiling import tile_wsi, tile_wsi_mask
from patho_pix.utils import convert_jpeg_to_tiff

# ---------------------------------------------------- #
#                    Configuration                     #
# ---------------------------------------------------- #
# Download links
url_img = "http://glioblastoma.alleninstitute.org/cgi-bin/imageservice?path=" + \
          "/external/gbm/prod0/0534338827/0534338827_annotation.aff&mime=1" + \
          "&fileout=100122048_1.jpg&zoom=9&top=20224&left=57888&width=15040&height=18048"
url_mask = "http://glioblastoma.alleninstitute.org/cgi-bin/imageservice?path=" + \
           "/external/gbm/prod0/0534338971/0534338971.aff&mime=1&fileout=100125374_2." + \
           "jpg&zoom=9&top=20608&left=55168&width=15040&height=18048"

path_img = None
path_mask = None

# Internal debugging links
# debug_path_img = "../data/dummy_wsi_01.image.jpg"
# debug_path_mask = "../data/dummy_wsi_01.mask.jpg"


# ---------------------------------------------------- #
#                   Unittest: Tiling                   #
# ---------------------------------------------------- #
class TileTEST(unittest.TestCase):
    # Download dummy data
    @classmethod
    def setUpClass(self):
        # Create temporary directory for dummy data
        self.tmp_data = tempfile.TemporaryDirectory(prefix="tmp.patho-pix.")
        # Download dummy image
        print("Downloading dummy image")
        response = requests.get(url_img)
        if response.status_code == 200:
            self.path_img = os.path.join(self.tmp_data.name, "image.jpg")
            with open(self.path_img, "wb") as fd:
                fd.write(response.content)
        # Download dummy mask
        print("Downloading dummy mask")
        response = requests.get(url_mask)
        if response.status_code == 200:
            self.path_mask = os.path.join(self.tmp_data.name, "mask.jpg")
            with open(self.path_mask, "wb") as fd:
                fd.write(response.content)

        # convert to tiff
        convert_jpeg_to_tiff(self.path_img, self.path_img.replace(".jpg", ".tiff"))
        convert_jpeg_to_tiff(self.path_mask, self.path_mask.replace(".jpg", ".tiff"))
        self.path_img = self.path_img.replace(".jpg", ".tiff")
        self.path_mask = self.path_mask.replace(".jpg", ".tiff")

    # ------------------------------------------------ #
    #                Test: Image Tiling                #
    # ------------------------------------------------ #
    def test_tile_image(self):
        tile_dir = tempfile.TemporaryDirectory(prefix="tmp.patho-pix.")
        wsi = load_wsi(self.path_img, tile_dir.name)
        tile_wsi(wsi)
        print(os.listdir(tile_dir.name))
        print(len(os.listdir(tile_dir.name)))
        self.assertEqual(len(os.listdir(tile_dir.name)), 37)

    # -------------------------------------------------#
    #            Test: Image and Mask Tiling           #
    # -------------------------------------------------#
    def test_load_image_and_mask(self):
        tile_dir_img = tempfile.TemporaryDirectory(prefix="tmp.patho-pix.")
        tile_dir_mask = tempfile.TemporaryDirectory(prefix="tmp.patho-pix.")
        wsi = load_wsi(self.path_img, tile_dir_img.name)
        mask = load_mask(self.path_mask, tile_dir_mask.name)
        tile_wsi_mask(wsi, mask)
        self.assertEqual(len(os.listdir(tile_dir_img.name)), 37)
