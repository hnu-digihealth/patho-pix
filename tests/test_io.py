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
# Internal libraries
from patho_pix.io import load_wsi, load_mask

#-----------------------------------------------------#
#                    Configuration                    #
#-----------------------------------------------------#
debug_path_img = "../data/dummy_wsi_01.image.jpg"
debug_path_mask = "../data/dummy_wsi_01.mask.jpg"

url_img = "https://glioblastoma.alleninstitute.org/cgi-bin/imageservice?path=/external/gbm/prod16/0534336905/0534336905_boundary.aff&mime=1&fileout=266289986_2.jpg&zoom=9&top=22304&left=25024&width=15040&height=18080"
url_mask = "https://glioblastoma.alleninstitute.org/cgi-bin/imageservice?path=/external/gbm/prod16/0534336761/0534336761_annotation.aff&mime=1&fileout=265854792_1.mask.jpg&zoom=9&top=23424&left=18112&width=15104&height=18176"

#-----------------------------------------------------#
#          Unittest: Input/Output Interface           #
#-----------------------------------------------------#
class IOTEST(unittest.TestCase):
    # Download 
    @classmethod
    def setUpClass(self):
        pass

    #-------------------------------------------------#
    #               Test: Image Loading               #
    #-------------------------------------------------#
    def test_load_image(self):
        wsi, path_tiles_wsi = load_wsi(debug_path_img)
        self.assertTrue(np.array_equal(wsi.level_dimensions(level=0), 
                                      (15040, 18080)))

    #-------------------------------------------------#
    #                Test: Mask Loading               #
    #-------------------------------------------------#
    def test_load_mask(self):
        mask, path_tiles_mask = load_mask(debug_path_mask)
        print(mask.level_dimensions(level=0))
        self.assertTrue(np.array_equal(mask.level_dimensions(level=0), 
                                      (15104, 18176)))