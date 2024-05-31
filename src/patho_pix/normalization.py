# Third Party
from histolab.stain_normalizer import (MacenkoStainNormalizer,
                                       ReinhardStainNormalizer)
from PIL import Image


def normalize_tile_reinhard(tile, path_target_img):
    target_img = Image.open(path_target_img)
    normalizer = ReinhardStainNormalizer()
    normalizer.fit(target_img)
    normalized_img = normalizer.transform(tile)
    return normalized_img


def normalize_tile_macenko(tile, path_target_img):
    target_img = Image.open(path_target_img)
    normalizer = MacenkoStainNormalizer()
    normalizer.fit(target_img)
    normalized_img = normalizer.transform(tile)
    return normalized_img
