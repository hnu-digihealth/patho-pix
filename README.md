# patho-pix: An Automated Modular WSI Preprocessing Pipeline for Digital Pathology
[![coverage](https://codecov.io/gh/hnu-digihealth/patho-pix/graph/badge.svg?token=3OCS8010KL)](https://codecov.io/gh/hnu-digihealth/patho-pix)
[![tests](https://github.com/hnu-digihealth/patho-pix/actions/workflows/test.yaml/badge.svg)](https://github.com/hnu-digihealth/patho-pix/actions/workflows/test.yaml)
[![PyPI version](https://badge.fury.io/py/patho-pix.svg)](https://badge.fury.io/py/patho-pix)
## Overview

patho-pix is a Python package designed to automate preprocessing of digital pathology images, leveraging existing processing frameworks into a modular pipeline. This package uses raw whole-slide-images (WSIs) and corresponding labels to preprocess the WSIs, It organizes and cleans up the input data into ready-to-use tiles and metadata, ensuring high-quality data for downstream machine learning analysis. Patho-pix integrates several key steps, including extraction of tissue regions ommiting background, tiling of the WSI, color normalization, artifact detection and removal and exportation of the tiles and metadata.

## Features

- **Tissue Region Extraction**: Identifies and focuses on tissue-covered regions, excluding the background of the image.
- **Tiling**: Divides WSIs into tiles of dynamic size (i.e. 1024x1024).
- **Color Normalization**: Color normalization across tiles for consistency.
- **Artifact Detection**: Identifies and removes tiles with artifacts (Upcoming feature).
- **Artifact Removal**: The pipeline provides two options to deal with artifacts. Corrupted tiles can either be thrown away and disregarded for further analysis. Alternatively a generative AI can be applied enhancing image quality by removing artifacts and filling in the missing data (Upcoming feature).
- **Export Tiles & Metadata**: Saves processed tiles and associated metadata for further use.

## Pipeline

![patho-pix Pipeline](https://github.com/hnu-digihealth/patho-pix/blob/main/media/patho-pix-pipeline.png?raw=true)

## Usage
To use patho pix you need to manually install the OpenSlide C-library as a dependency.
- Mac (with homebrew): `brew install openslide`.
- Linux (with the package manager of your choice): e.g., Ubuntu: sudo apt install `openslide-tools`
- Windows: Take a look at the [OpenSlide Docu](https://openslide.org)

## Contributing
If you want to support the patho-pix project please take a look at the [CONTRIBUTING](CONTRIBUTING.md) guide.

### For VSCode
You can use the provided Dev Container to quick start your development process of the patho pix project. Install `Docker Desktop` and VS Code Extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
