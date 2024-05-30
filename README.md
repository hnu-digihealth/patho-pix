# patho-pix: An Automated WSI Preprocessing Pipeline for Digital Pathology

## Overview

patho-pix is a Python package designed to automate preprocessing of digital pathology images, leveraging existing processing frameworks into a modular pipeline. This package uses raw whole-slide-images (WSIs) and corresponding labels preprocesses the WSI, organizing the input data into ready-to-use tiles and metadata, ensuring high-quality data for further ML-analysis. Patho-pix integrates several key steps, including extraction of tissue regions ommiting background, tiling of the WSI, artifact detection and removal, exportation of tiles and metadata, and color normalization.

## Features

- **Tissue Region Extraction**: Identifies and focuses on tissue-covered regions, excluding the background of the image.
- **Tiling**: Divides WSIs into tiles of dynamic size.
- **Artifact Detection**: Identifies and removes tiles with artifacts.
- **Generative AI**: Enhances image quality by removing artifacts and filling in the missing data (Upcoming feature).
- **Export Tiles & Metadata**: Saves processed tiles and associated metadata for further use.
- **Color Normalization**: Color normalization across tiles for consistency.

Please read the [CONTRIBUTING](CONTRIBUTING.md) guide.

## Pipeline

![patho-pix Pipeline](./media/patho-pix-pipeline.png)
## Setup

Install OpenSlide:

Mac (with homebrew): `brew install openslide`.

Install `pdm`.
Then run `pdm install --verbose`.  
Then install patho-pix: `pip install patho_pix`.

## For VSCode

Install `Docker Desktop` and VS Code Extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).




# patho-pix
[![coverage](https://codecov.io/gh/hnu-digihealth/patho-pix/graph/badge.svg?token=3OCS8010KL)](https://codecov.io/gh/hnu-digihealth/patho-pix)
[![tests](https://github.com/hnu-digihealth/patho-pix/actions/workflows/test.yaml/badge.svg)](https://github.com/hnu-digihealth/patho-pix/actions/workflows/test.yaml)

Please read the [CONTRIBUTING](CONTRIBUTING.md) guide.



