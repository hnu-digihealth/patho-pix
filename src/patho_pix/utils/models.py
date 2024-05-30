import torch.nn as nn
from torchvision import models
import torch.nn.functional as F


class ResNet18(nn.Module):
    def __init__(self, n_classes):
        super(ResNet18, self).__init__()

        resnet = models.resnet18()
        self.resnet = nn.Sequential(*list(resnet.children())[:-1])
        self.down = nn.Linear(512, n_classes)

    def embedding(self, x):
        x = self.resnet(x)
        x = F.relu(x.view(x.size(0), x.size(1)))
        x = self.down(x)
        return x
