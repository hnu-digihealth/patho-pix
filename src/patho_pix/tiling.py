# =========================================================== #
#  Author:       Hackathon UKSH Team 14 - Patho-Pix           #
#  Copyright:    Patho-Pix Team - 2024                        #
# =========================================================== #
# ---------------------------------------------------- #
#                   Library imports                    #
# ---------------------------------------------------- #
# Third Party
from histolab.masks import TissueMask
from histolab.tiler import GridTiler

# patho_pix
from patho_pix.utils import AwesomeTiler


# ---------------------------------------------------- #
#     Apply tiling base on Tissue Mask - Only Image    #
# ---------------------------------------------------- #
def tile_wsi(wsi, tile_size=(1024, 1024)):
    # Initialize Tiler
    wsi_tiler = GridTiler(
        tile_size=tile_size,
        check_tissue=True,
        tissue_percent=10.0,
        prefix="patho-fix.",
        suffix=".png",
    )
    # extract tile
    wsi_tiler.extract(wsi, extraction_mask=TissueMask())


# ---------------------------------------------------- #
#    Apply tiling base on Tissue Mask - Image + Mask   #
# ---------------------------------------------------- #
def tile_wsi_mask(wsi_img, wsi_label, tile_size=(1024, 1024)):
    # Initialize Tiler
    wsi_tiler = AwesomeTiler(
        tile_size=tile_size,
        check_tissue=True,
        tissue_percent=10.0,
        prefix="patho-fix.",
        suffix=".png",
    )
    # extract tile
    metadata = wsi_tiler.extract(wsi_img, wsi_label, extraction_mask=TissueMask())
    return metadata
