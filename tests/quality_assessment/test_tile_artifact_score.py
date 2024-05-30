# =========================================================== #
#  Author:       Hackathon UKSH Team 14 - Patho-Pix           #
#  Copyright:    Patho-Pix Team - 2024                        #
# =========================================================== #
# -----------------------------------------------------#
#                   Library imports                    #
# -----------------------------------------------------#
import unittest
from PIL import Image

from patho_pix.quality_assessment import asses_tile_artifact_score


# ---------------------------------------------------- #
#        Unittest: Artifact Score Calculation          #
# ---------------------------------------------------- #
class TileArtifactScoreTest(unittest.TestCase):
    # -------------------------------------------------#
    #         Test: artifact score calculation         #
    # -------------------------------------------------#
    def test_asses_tile_artifact_score_with_artifacts(self):
        img = Image.open('tests/image_files/oof_and_fold.png')
        res = asses_tile_artifact_score(img, 'models/checkpoint_ts_2.pth', None)
        print(res)
        self.assertTrue(res is not None)

    def test_asses_tile_artifact_score_without_artifacts(self):
        img = Image.open('tests/image_files/oof_and_fold.png')
        res = asses_tile_artifact_score(img, 'models/checkpoint_ts_2.pth', None)
        print(res)
        self.assertTrue(res is not None)
