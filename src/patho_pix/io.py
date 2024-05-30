# =========================================================== #
#  Author:       Hackathon UKSH Team 14 - Patho-Pix           #
#  Copyright:    Patho-Pix Team - 2024                        #
# =========================================================== #
# -----------------------------------------------------#
#                   Library imports                    #
# -----------------------------------------------------#
# Standard Library
import tempfile

# Third Party
from histolab.slide import Slide


# -----------------------------------------------------#
#                    Image Loader                      #
# -----------------------------------------------------#
def load_wsi(path, use_largeimage=True):
    # Create temporary directory for WSI scan tiles later
    pathdir_tiles_img = tempfile.TemporaryDirectory(
        prefix="patho-pix.tmp.", suffix=".tiles_img"
    )
    # Load WSI scan via histolab
    wsi_slide = Slide(
        path=path, 
        processed_path=pathdir_tiles_img.name, 
        use_largeimage=use_largeimage
    )
    # Return histolab WSI
    return wsi_slide, pathdir_tiles_img


# -----------------------------------------------------#
#                     Mask Loader                      #
# -----------------------------------------------------#
def load_mask(path, use_largeimage=True):
    # Create temporary directory for WSI mask tiles later
    pathdir_tiles_mask = tempfile.TemporaryDirectory(
        prefix="patho-pix.tmp.", suffix=".tiles_mask"
    )
    # Load WSI mask via histolab
    wsi_slide = Slide(
        path=path, 
        processed_path=pathdir_tiles_mask.name, 
        use_largeimage=use_largeimage
    )
    # Return histolab WSI
    return wsi_slide, pathdir_tiles_mask
