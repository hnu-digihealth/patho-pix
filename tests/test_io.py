#==============================================================================#
#  Author:       Hackathon UKSH Team 14 - Patho-Pix                            #
#  Copyright:    Patho-Pix Team - 2024                                         #
#==============================================================================#
#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
import unittest
import os
import numpy as np
import requests
import tempfile
# Internal libraries
from patho_pix.io import load_wsi, load_mask

#-----------------------------------------------------#
#                    Configuration                    #
#-----------------------------------------------------#
# Download links
url_img = "http://glioblastoma.alleninstitute.org/cgi-bin/imageservice?path=/external/gbm/prod16/0534336905/0534336905_boundary.aff&mime=1&fileout=266289986_2.jpg&zoom=9&top=22304&left=25024&width=15040&height=18080"
url_mask = "http://glioblastoma.alleninstitute.org/cgi-bin/imageservice?path=/external/gbm/prod16/0534336761/0534336761_annotation.aff&mime=1&fileout=265854792_1.mask.jpg&zoom=9&top=23424&left=18112&width=15104&height=18176"
path_img = None
path_mask = None

# Internal debugging links
# debug_path_img = "../data/dummy_wsi_01.image.jpg"
# debug_path_mask = "../data/dummy_wsi_01.mask.jpg"

#-----------------------------------------------------#
#          Unittest: Input/Output Interface           #
#-----------------------------------------------------#
class IOTEST(unittest.TestCase):
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
                
    #-------------------------------------------------#
    #               Test: Image Loading               #
    #-------------------------------------------------#
    def test_load_image(self):
        print(os.path.exists(self.path_img))
        wsi, path_tiles_wsi = load_wsi(self.path_img)
        self.assertTrue(np.array_equal(wsi.level_dimensions(level=0), 
                                      (15040, 18080)))

    #-------------------------------------------------#
    #                Test: Mask Loading               #
    #-------------------------------------------------#
    def test_load_mask(self):
        print(os.path.exists(self.path_mask))
        mask, path_tiles_mask = load_mask(self.path_mask)
        self.assertTrue(np.array_equal(mask.level_dimensions(level=0), 
                                      (15104, 18176)))