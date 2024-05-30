# =========================================================== #
#  Author:       Hackathon UKSH Team 14 - Patho-Pix           #
#  Copyright:    Patho-Pix Team - 2024                        #
# =========================================================== #
# ---------------------------------------------------- #
#                   Library imports                    #
# ---------------------------------------------------- #
from histolab.tiler import GridTiler
from histolab.masks import TissueMask


# ---------------------------------------------------- #
#           Apply Tiling base on Tissue Mask           #
# ---------------------------------------------------- #
def tile_wsi(wsi, tile_size=(1024, 1024)):
    # Initialize Tiler
    wsi_tiler = GridTiler(tile_size=tile_size,
                            check_tissue=True,
                            tissue_percent=80.0,
                            prefix="patho-fix.",
                            suffix=".png"
                            )
    # extract tile
    wsi_tiler.extract(wsi,
                      extraction_mask=TissueMask()
                      )
