import torch
from torch.utils.data import Dataset
import json
import os
import numpy as np #
from scipy.io import loadmat
import h5py  # change_1
import matplotlib.pyplot as plt


class PureDataset(Dataset):
    """
    A PyTorch Dataset class to be used in a PyTorch DataLoader to create batches.
    """

    def __init__(self, data_folder, split):
        """
        :param data_folder: folder where data files are stored  #存储数据文件的文件夹
        :param split: split, one of 'TRAIN' or 'TEST'
        """
        self.split = split
        self.data_folder = data_folder

        # Read data files
        with open(os.path.join(data_folder, self.split + '_image.json'), 'r') as j:
            self.tensors = json.load(j)
        with open(os.path.join(data_folder, self.split + '_label.json'), 'r') as j:
            self.gtPPGs = json.load(j)

        assert len(self.tensors) == len(self.gtPPGs)

    def __len__(self):
        return len(self.tensors)

    def __getitem__(self, idx):
        # Read image
        tensorFileName = self.tensors[idx]     #.json文件中的内容是一个个路径
        stRep = loadmat(tensorFileName)
        stRep_0 = stRep['layer0']
        stRep_1 = stRep['layer1']
        stRep_2 = stRep['layer2']
        stRep_3 = stRep['layer3']
        # stRep_4 = stRep['layer4']

        stRep_0 = stRep_0 / 255
        stRep_1 = stRep_1 / 255
        stRep_2 = stRep_2 / 255
        stRep_3 = stRep_3 / 255
        # stRep_4 = stRep_4 / 255
        # stRep = np.array([stRep])

        stRep_0 = torch.FloatTensor(stRep_0)
        stRep_1 = torch.FloatTensor(stRep_1)
        stRep_2 = torch.FloatTensor(stRep_2)
        stRep_3 = torch.FloatTensor(stRep_3)
        # stRep_4 = torch.FloatTensor(stRep_4)
        # stRep = stRep.permute([0, 2, 1, 3, 4])

        # Read label
        gtPPGFile = self.gtPPGs[idx]
        gtPPG = loadmat(gtPPGFile)
        gtPPG = gtPPG['ppgSeg']
        gtPPG = gtPPG - np.mean(gtPPG)
        gtPPG = gtPPG / np.std(gtPPG)
        gtPPG = torch.FloatTensor(gtPPG)

        return stRep_0, stRep_1, stRep_2, stRep_3, gtPPG

