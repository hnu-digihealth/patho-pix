import numpy as np
import glob
import os
import cv2
import os.path as path
import torch
import torchvision.models as models
import torchvision.transforms as transforms

def eval_quality(tile, QA_model):
    """
    Evaluate the quality of a given image tile using a pretrained Quality Assessment (QA) model.

    Args:
        tile (PIL.Image or numpy.ndarray): The image tile to be evaluated. Expected to be a PIL image or a NumPy array.
        QA_model (torch.nn.Module): A pretrained PyTorch model that predicts various quality metrics.

    Returns:
        dict: A dictionary containing quality assessment metrics including usability, normal appearance,
              focus issues, staining issues, tissue folding, other artifacts, and a validity flag.

    Description:
        The function first resizes the input tile to 224x224 pixels, which is a common input size for deep learning models.
        It then applies standard normalization and conversion to a PyTorch tensor. The image is then fed into the QA model,
        and the output is clipped to the range [0, 1] to ensure valid probability values. The final output includes
        a set of predefined keys corresponding to different quality metrics, with an additional 'valid_data' key set to 1
        to indicate the validity of the output.
    """
    # Define normalization and tensor conversion transforms
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    totensor = transforms.ToTensor()

    # Preprocess the tile: resize, convert to tensor, and normalize
    tile = cv2.resize(np.array(tile), (224, 224), interpolation=cv2.INTER_CUBIC)
    tile = normalize(totensor(tile)).type(torch.FloatTensor)

    # Keys for the output dictionary, corresponding to different assessment metrics
    keys = ['usability (1 = highly usable)',
            'normal (1=no artifacts present)',
            'focus_issues (1=severe focus issues)',
            'staining_issues (1=severe staining issues)',
            'tissue_folding (1=tissue foldings present)',
            'other_artefacts (1=artefacts present)',
            'valid_data (1=valid data)']

    # Disable gradient calculations, predict using the QA model, process output
    with torch.no_grad():
        out = QA_model.embedding(tile.unsqueeze(0)).squeeze(0).cpu()
        out = out.data.numpy().clip(0, 1)  # Ensure all outputs are between 0 and 1

    # Pad the output array to match the number of keys (adding 'valid_data')
    out = np.pad(out, (0, 1), mode='constant', constant_values=1)

    # Create a dictionary from keys and outputs
    return dict(zip(keys, out))

def instantiate_model():

    # QA_model = ResNet18(n_classes=6)
    model = models.resnet18(pretrained=False)#, n_classes=6)

    # print(os.path.isfile('model/checkpoint_106.pth'))

    checkpoint = torch.load(
        'model/checkpoint_106.pth',
        map_location=torch.device('cpu')
    )

    state_dict = checkpoint['state_dict']
    new_state_dict = state_dict
    from collections import OrderedDict
    # new_state_dict = OrderedDict()
    # for k, v in state_dict.items():
    #   name = k.replace("module.", "")  # remove 'module.' if it exists
    #   new_state_dict[name] = v

    # model.load_state_dict(checkpoint['state_dict'])
    model.load_state_dict(new_state_dict, strict=False)

    # num_features = model.fc.in_features
    # model.fc = torch.nn.Linear(num_features, 6)

    model.eval()
    # model.cpu()

    return model


tile = cv2.imread('media/test-images-steps/oof_and_fold.jpg')

QA_model = instantiate_model()
result = eval_quality(tile, QA_model)

print(result)
