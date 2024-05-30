# =========================================================== #
#  Author:       Hackathon UKSH Team 14 - Patho-Pix           #
#  Copyright:    Patho-Pix Team - 2024                        #
# =========================================================== #
# -----------------------------------------------------#
#                   Library imports                    #
# -----------------------------------------------------#
# Standard Library
import os

# Third Party
from histolab.slide import Slide


# -----------------------------------------------------#
#                    Image Loader                      #
# -----------------------------------------------------#
def load_wsi(path_slide, path_tile_dir, use_largeimage=False):
    # Create path tile directory
    if not os.path.exists(path_tile_dir):
        os.mkdir(path_tile_dir)
    # Load WSI scan via histolab
    wsi_slide = Slide(
        path=path_slide, processed_path=path_tile_dir, use_largeimage=use_largeimage
    )
    # Return histolab WSI
    return wsi_slide


# -----------------------------------------------------#
#                     Mask Loader                      #
# -----------------------------------------------------#
def load_mask(path_slide, path_tile_dir, use_largeimage=False):
    # Create path tile directory
    if not os.path.exists(path_tile_dir):
        os.mkdir(path_tile_dir)
    # Load WSI mask via histolab
    wsi_slide = Slide(
        path=path_slide, processed_path=path_tile_dir, use_largeimage=use_largeimage
    )
    # Return histolab WSI
    return wsi_slide
