# =========================================================== #
#  Author:       Hackathon UKSH Team 14 - Patho-Pix           #
#  Copyright:    Patho-Pix Team - 2024                        #
# =========================================================== #
# ---------------------------------------------------- #
#                   Library imports                    #
# ---------------------------------------------------- #
# Standard Library
import logging
import os
from typing import Tuple

# Third Party
import numpy as np
from histolab.exceptions import TileSizeOrCoordinatesError
from histolab.masks import BiggestTissueBoxMask, BinaryMask
from histolab.slide import Slide
from histolab.tile import Tile
from histolab.tiler import Tiler
from histolab.types import CoordinatePair
from histolab.util import (rectangle_to_mask, region_coordinates,
                           regions_from_binary_mask, regions_to_binary_mask,
                           scale_coordinates)

logger = logging.getLogger("tiler")

COORDS_WITHIN_EXTRACTION_MASK_THRESHOLD = 0.8


# ---------------------------------------------------- #
#            Custom GridTiler: AwesomeTiler            #
# ---------------------------------------------------- #
class AwesomeTiler(Tiler):
    """Extractor of tiles arranged in a grid, at the given level, with the given size.

    Arguments
    ---------
    tile_size : Tuple[int, int]
        (width, height) of the extracted tiles.
    level : int, optional
        Level from which extract the tiles. Default is 0.
        Superceded by mpp if the mpp argument is provided.
    check_tissue : bool, optional
        Whether to check if the tile has enough tissue to be saved. Default is True.
    tissue_percent : float, optional
        Number between 0.0 and 100.0 representing the minimum required percentage of
        tissue over the total area of the image, default is 80.0. This is considered
        only if ``check_tissue`` equals to True.
    pixel_overlap : int, optional
       Number of overlapping pixels (for both height and width) between two adjacent
       tiles. If negative, two adjacent tiles will be strided by the absolute value of
       ``pixel_overlap``. Default is 0.
    prefix : str, optional
        Prefix to be added to the tile filename. Default is an empty string.
    suffix : str, optional
        Suffix to be added to the tile filename. Default is '.png'
    mpp : float, optional
        Micron per pixel resolution of extracted tiles. Takes precedence over level.
        Default is None.
    """

    def __init__(
        self,
        tile_size: Tuple[int, int],
        level: int = 0,
        check_tissue: bool = True,
        tissue_percent: float = 80.0,
        pixel_overlap: int = 0,
        prefix: str = "",
        suffix: str = ".png",
        mpp: float = None,
    ):
        self.tile_size = tile_size
        self.final_tile_size = tile_size
        self.level = level if mpp is None else 0
        self.mpp = mpp
        self.check_tissue = check_tissue
        self.tissue_percent = tissue_percent
        self.pixel_overlap = pixel_overlap
        self.prefix = prefix
        self.suffix = suffix

    def extract(
        self,
        wsi_img: Slide,
        wsi_label: Slide,
        extraction_mask: BinaryMask = BiggestTissueBoxMask(),
        log_level: str = "INFO",
    ) -> None:
        """Extract tiles arranged in a grid and save them to disk, following this
        filename pattern:
        `{prefix}tile_{tiles_counter}_level{level}_{x_ul_wsi}-{y_ul_wsi}-{x_br_wsi}-{y_br_wsi}{suffix}`

        Parameters
        ----------
        wsi_img : Slide
            Image slide from which to extract the tiles
        wsi_label : Slide
            Mask slide from which to extract the tiles
        extraction_mask : BinaryMask, optional
            BinaryMask object defining how to compute a binary mask from a Slide.
            Default `BiggestTissueBoxMask`.
        log_level : str, {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
            Threshold level for the log messages. Default "INFO"

        Raises
        ------
        TileSizeError
            If the tile size is larger than the slide size
        LevelError
            If the level is not available for the slide
        """
        level = logging.getLevelName(log_level)
        logger.setLevel(level)
        self._validate_level(wsi_img)
        self.tile_size = self._tile_size(wsi_img)
        self.pixel_overlap = int(self._scale_factor(wsi_img) * self.pixel_overlap)
        self._validate_tile_size(wsi_img)

        grid_tiles = self._tiles_generator(wsi_img, extraction_mask)
        tiles_counter = 0
        metadata = {}
        for tiles_counter, (tile, tile_wsi_coords) in enumerate(grid_tiles):
            # Domi edit: wsi_img tile
            tile_filename = self._tile_filename(tile_wsi_coords, tiles_counter)
            full_tile_path = os.path.join(wsi_img.processed_path, tile_filename)
            tile.save(full_tile_path)
            logger.info(f"\t Image Tile {tiles_counter} saved: {tile_filename}")
            # Domi edit: wsi_label tile
            mask_tile = self._tile_mask_extract(wsi_label, tile_wsi_coords)
            tile_filename = self._tile_filename(tile_wsi_coords, tiles_counter)
            full_tile_path = os.path.join(wsi_label.processed_path, tile_filename)
            mask_tile.save(full_tile_path)
            logger.info(f"\t Mask Tile {tiles_counter} saved: {tile_filename}")
            # Domi edit: access metadata
            metadata[tile_filename] = [
                tile.tissue_ratio,
                self.tile_size,
                tile_wsi_coords[0:2]
            ]

        logger.info(f"{tiles_counter} Grid Tiles have been saved.")
        return metadata

    @property
    def tile_size(self) -> Tuple[int, int]:
        """(width, height) of the extracted tiles."""
        return self._valid_tile_size

    @tile_size.setter
    def tile_size(self, tile_size_: Tuple[int, int]):
        if tile_size_[0] < 1 or tile_size_[1] < 1:
            raise ValueError(f"Tile size must be greater than 0 ({tile_size_})")
        self._valid_tile_size = tile_size_

    # ------- implementation helpers -------

    @staticmethod
    def _are_coordinates_within_extraction_mask(
        tile_thumb_coords: CoordinatePair,
        binary_mask_region: np.ndarray,
    ) -> bool:
        """Chack whether the ``tile_thumb_coords`` are inside of ``binary_mask_region``.

        Return True if 80% of the tile area defined by tile_thumb_coords is inside the
        area of the ``binary_mask_region.

        Parameters
        ----------
        tile_thumb_coords : CoordinatePair
            Coordinates of the tile at thumbnail dimension.
        binary_mask_region : np.ndarray
            Binary mask with True inside of the tissue region considered.

        Returns
        -------
        bool
            Whether the 80% of the tile area defined by tile_thumb_coords is inside the
            area of the ``binary_mask_region.
        """

        tile_thumb_mask = rectangle_to_mask(
            dims=binary_mask_region.shape, vertices=tile_thumb_coords
        )

        tile_in_binary_mask = binary_mask_region & tile_thumb_mask

        tile_area = np.count_nonzero(tile_thumb_mask)
        tile_in_binary_mask_area = np.count_nonzero(tile_in_binary_mask)

        return tile_area > 0 and (
            tile_in_binary_mask_area / tile_area
            > COORDS_WITHIN_EXTRACTION_MASK_THRESHOLD
        )

    def _grid_coordinates_from_bbox_coordinates(
        self,
        bbox_coordinates_lvl: CoordinatePair,
        slide: Slide,
        binary_mask_region: np.ndarray,
    ) -> CoordinatePair:
        """Generate Coordinates at level 0 of grid tiles within a tissue box.

        Parameters
        ----------
        bbox_coordinates_lvl : CoordinatePair
            Coordinates of the tissue box from which to calculate the coordinates of the
            tiles.
        slide : Slide
            Slide from which to calculate the coordinates.
        binary_mask_region : np.ndarray
            Binary mask corresponding to the connected component (region) considered.

        Notes
        -----
        This method needs to be called for every connected component (region) within the
        extraction mask.

        Yields
        -------
        Iterator[CoordinatePair]
            Iterator of tiles' CoordinatePair
        """
        tile_w_lvl, tile_h_lvl = self.tile_size

        n_tiles_row = self._n_tiles_row(bbox_coordinates_lvl)
        n_tiles_column = self._n_tiles_column(bbox_coordinates_lvl)

        for i in range(n_tiles_row):
            for j in range(n_tiles_column):
                x_ul_lvl = (
                    bbox_coordinates_lvl.x_ul + tile_w_lvl * i - self.pixel_overlap * i
                )
                y_ul_lvl = (
                    bbox_coordinates_lvl.y_ul + tile_h_lvl * j - self.pixel_overlap * j
                )

                x_ul_lvl = np.clip(x_ul_lvl, bbox_coordinates_lvl.x_ul, None)
                y_ul_lvl = np.clip(y_ul_lvl, bbox_coordinates_lvl.y_ul, None)

                x_br_lvl = x_ul_lvl + tile_w_lvl
                y_br_lvl = y_ul_lvl + tile_h_lvl

                tile_lvl_coords = CoordinatePair(x_ul_lvl, y_ul_lvl, x_br_lvl, y_br_lvl)
                tile_thumb_coords = scale_coordinates(
                    reference_coords=tile_lvl_coords,
                    reference_size=slide.level_dimensions(level=self.level),
                    target_size=binary_mask_region.shape[::-1],
                )

                if self._are_coordinates_within_extraction_mask(
                    tile_thumb_coords, binary_mask_region
                ):
                    tile_wsi_coords = scale_coordinates(
                        reference_coords=tile_lvl_coords,
                        reference_size=slide.level_dimensions(level=self.level),
                        target_size=slide.level_dimensions(level=0),
                    )
                    yield tile_wsi_coords

    def _grid_coordinates_generator(
        self, slide: Slide, extraction_mask: BinaryMask = BiggestTissueBoxMask()
    ) -> CoordinatePair:
        """Generate Coordinates at level 0 of grid tiles within the tissue.

        Parameters
        ----------
        slide : Slide
            Slide from which to calculate the coordinates. Needed to calculate the
            tissue area.
        extraction_mask : BinaryMask, optional
            BinaryMask object defining how to compute a binary mask from a Slide.
            Default `BiggestTissueBoxMask`.

        Yields
        -------
        Iterator[CoordinatePair]
            Iterator of tiles' CoordinatePair
        """
        binary_mask = extraction_mask(slide)

        regions = regions_from_binary_mask(binary_mask)
        for region in regions:
            bbox_coordinates_thumb = region_coordinates(region)  # coords of the bbox
            bbox_coordinates_lvl = scale_coordinates(
                bbox_coordinates_thumb,
                binary_mask.shape[::-1],
                slide.level_dimensions(self.level),
            )

            binary_mask_region = regions_to_binary_mask([region], binary_mask.shape)

            yield from self._grid_coordinates_from_bbox_coordinates(
                bbox_coordinates_lvl, slide, binary_mask_region
            )

    def _n_tiles_column(self, bbox_coordinates: CoordinatePair) -> int:
        """Return the number of tiles which can be extracted in a column.

        Parameters
        ----------
        bbox_coordinates : CoordinatePair
            Coordinates of the tissue box

        Returns
        -------
        int
            Number of tiles which can be extracted in a column.
        """
        return (bbox_coordinates.y_br - bbox_coordinates.y_ul) // (
            self.tile_size[1] - self.pixel_overlap
        )

    def _n_tiles_row(self, bbox_coordinates: CoordinatePair) -> int:
        """Return the number of tiles which can be extracted in a row.

        Parameters
        ----------
        bbox_coordinates : CoordinatePair
            Coordinates of the tissue box

        Returns
        -------
        int
            Number of tiles which can be extracted in a row.
        """
        return (bbox_coordinates.x_br - bbox_coordinates.x_ul) // (
            self.tile_size[0] - self.pixel_overlap
        )

    def _tiles_generator(
        self, slide: Slide, extraction_mask: BinaryMask = BiggestTissueBoxMask()
    ) -> Tuple[Tile, CoordinatePair]:
        """Generator of tiles arranged in a grid.

        Parameters
        ----------
        slide : Slide
            Slide from which to extract the tiles
        extraction_mask : BinaryMask, optional
            BinaryMask object defining how to compute a binary mask from a Slide.
            Default `BiggestTissueBoxMask`.

        Yields
        -------
        Tile
            Extracted tile
        CoordinatePair
            Coordinates of the slide at level 0 from which the tile has been extracted
        """
        grid_coordinates_generator = self._grid_coordinates_generator(
            slide, extraction_mask
        )
        for coords in grid_coordinates_generator:
            try:
                tile = slide.extract_tile(
                    coords,
                    tile_size=self.final_tile_size,
                    mpp=self.mpp,
                    level=self.level if self.mpp is None else None,
                )
            except TileSizeOrCoordinatesError:
                continue

            if not self.check_tissue or tile.has_enough_tissue(self.tissue_percent):
                yield tile, coords

    # Domi Function - hacking with no docs
    def _tile_mask_extract(self, slide: Slide, coords):
        tile = slide.extract_tile(
            coords,
            tile_size=self.final_tile_size,
            mpp=self.mpp,
            level=self.level if self.mpp is None else None,
        )
        return tile
