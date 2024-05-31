# patho-pix: An Automated WSI Preprocessing Pipeline for Digital Pathology

## Overview

patho-pix is a Python package designed to automate preprocessing of digital pathology images, leveraging existing processing frameworks into a modular pipeline. This package uses raw whole-slide-images (WSIs) and corresponding labels to preprocess the WSIs, It organizes and cleans up the input data into ready-to-use tiles and metadata, ensuring high-quality data for downstream machine learning analysis. Patho-pix integrates several key steps, including extraction of tissue regions ommiting background, tiling of the WSI, color normalization, artifact detection and removal and exportation of the tiles and metadata. 

## Features

- **Tissue Region Extraction**: Identifies and focuses on tissue-covered regions, excluding the background of the image.
- **Tiling**: Divides WSIs into tiles of dynamic size (i.e. 1024x1024).
- **Color Normalization**: Color normalization across tiles for consistency.
- **Artifact Detection**: Identifies and removes tiles with artifacts (Upcoming feature).
- **Artifact Removal**: The pipeline provides two options to deal with artifacts. Corrupted tiles can either be thrown away and disregarded for further analysis. Alternatively a generative AI can be applied enhancing image quality by removing artifacts and filling in the missing data (Upcoming feature).
- **Export Tiles & Metadata**: Saves processed tiles and associated metadata for further use.

Please read the [CONTRIBUTING](CONTRIBUTING.md) guide.

## Pipeline

![patho-pix Pipeline](./media/patho-pix-pipeline.png)
## Installation

For this package OpenSlide is required and needs to be installed first:
Mac (with homebrew): `brew install openslide`.

The the package manager `pdm` needs to be installed.
Then run `pdm install --verbose`.  
Then install the package `patho-pix` using `pip install patho_pix`.

## For VSCode

Install `Docker Desktop` and VS Code Extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).




# patho-pix
[![coverage](https://codecov.io/gh/hnu-digihealth/patho-pix/graph/badge.svg?token=3OCS8010KL)](https://codecov.io/gh/hnu-digihealth/patho-pix)
[![tests](https://github.com/hnu-digihealth/patho-pix/actions/workflows/test.yaml/badge.svg)](https://github.com/hnu-digihealth/patho-pix/actions/workflows/test.yaml)

Please read the [CONTRIBUTING](CONTRIBUTING.md) guide.



