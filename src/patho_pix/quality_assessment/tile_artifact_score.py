import numpy as np
import cv2
import torch
from torchvision import transforms
from patho_pix.utils import ResNet18


def asses_tile_artifact_score(tile, model_path, metadata):
    QA_model = init_model(model_path)

    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    totensor = transforms.ToTensor()

    # Preprocess the tile: resize, convert to tensor, and normalize
    tile = cv2.resize(np.array(tile), (224, 224), interpolation=cv2.INTER_CUBIC)
    tile = normalize(totensor(tile)).type(torch.FloatTensor)

    # Keys for the output dictionary, corresponding to different assessment metrics
    keys = ['usability',
            'normal',
            'focus_issues',
            'staining_issues',
            'tissue_folding',
            'other_artefacts',
            'valid_data']

    with torch.no_grad():
        out = QA_model.embedding(tile.unsqueeze(0)).squeeze(0).cpu()
        out = out.data.numpy().clip(0, 1)  # Ensure all outputs are between 0 and 1

    # Pad the output array to match the number of keys (adding 'valid_data')
    out = np.pad(out, (0, 1), mode='constant', constant_values=1)

    # Create a dictionary from keys and outputs
    return dict(zip(keys, out))


def init_model(path):
    QA_model = ResNet18(n_classes=6)
    checkpoint = torch.load(path, map_location=torch.device('cpu'))

    QA_model.load_state_dict(checkpoint['state_dict'])
    QA_model.eval()
    QA_model.cpu()
    return QA_model
