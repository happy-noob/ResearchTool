import os
import cv2
import numpy as np
import torch
from torchvision.datasets import ImageFolder
import torchvision
import torch.utils.data.dataloader

def getStat(train_data):
    '''
    Compute mean and variance for training data
    :param train_data: 自定义类Dataset(或ImageFolder即可)
    :return: (mean, std)
    '''
    print('Compute mean and variance for training data.')
    print(len(train_data))
    train_loader = torch.utils.data.DataLoader(
        train_data, batch_size=1, shuffle=False, num_workers=0,
        pin_memory=True)
    mean = torch.zeros(3)
    std = torch.zeros(3)
    for X, _ in train_loader:
        for d in range(3):
            mean[d] += X[:, d, :, :].mean()
            std[d] += X[:, d, :, :].std()
    mean.div_(len(train_data))
    std.div_(len(train_data))
    return list(mean.numpy()), list(std.numpy())


# if __name__ == '__main__':
#     train_dataset = ImageFolder(root=r'./datasets', transform= torchvision.transforms.ToTensor())
#     print(getStat(train_dataset))

#[0.40,0.40,0.40],[0.25,0.25,0.25]

# img_mean [206.13099684952792, 205.48790015417205, 206.03535884143093]
# img_std [71.01260148469036, 72.11945500258794, 71.3830043493716]

# ([0.8083574, 0.8058346, 0.8079817], [0.27848127, 0.28282198, 0.2799339])