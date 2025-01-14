import warnings

warnings.filterwarnings('ignore')

import os
import sys

parent = os.path.abspath(os.path.curdir)
sys.path.insert(1, parent)

import cv2
import numpy as np
import glob
import random
from tqdm import tqdm

import torch
import torch.nn as nn
from torch.utils.data import Dataset
from torchvision import transforms as T

from src.utils import get_padding
from src.constant import TRAIN_FRAGMENTS_PATH


class DatasetVesuvius(Dataset):
    def __init__(self, fragments, tile_size, num_slices, slices_list, start_slice, reverse_slices, selection_thr, augmentation, device, overlap):
        self.fragments = fragments
        self.tile_size = tile_size
        self.num_slices = num_slices
        self.slices_list = slices_list
        self.start_slice = start_slice
        self.reverse_slices = reverse_slices
        self.selection_thr = selection_thr
        self.augmentation = augmentation
        self.device = device

        self.overlap = overlap
        self.set_path = TRAIN_FRAGMENTS_PATH
        self.slices = self.make_slices()
        self.data, self.items = self.make_data()

        self.transforms = T.RandomApply(
            nn.ModuleList([
                T.RandomRotation(180),
                T.RandomPerspective(),
                T.ElasticTransform(alpha=500.0, sigma=10.0),
                T.RandomHorizontalFlip(),
                T.RandomVerticalFlip()
            ]), p=0.5
        )

    def make_slices(self):
        total_slices = 65
        slices = [i for i in range(total_slices)]

        if self.slices_list:
            slices = self.slices_list
        else:
            slices = sorted(slices[self.start_slice:self.start_slice+self.num_slices], reverse=self.reverse_slices)

        return slices

    def make_mask(self, fragment_path):
        mask_path = os.path.join(fragment_path, 'inklabels.png')
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        shape = (self.num_slices, mask.shape[0], mask.shape[1])
        padding = get_padding(mask.shape, self.tile_size)
        mask_pad = np.pad(mask, padding)

        return mask_pad, shape, padding

    def make_image(self, fragment_path, shape, padding):
        image = np.zeros(shape=shape, dtype=np.uint8)
        slices_files = sorted(glob.glob(os.path.join(fragment_path, 'surface_volume/*.tif')))
        slices_path = [slices_files[i] for i in self.slices]

        print(f'\nMake image from {fragment_path}')
        for i, slice_path in tqdm(enumerate(slices_path), total=len(slices_path)):
            image[i, ...] = cv2.imread(slice_path, cv2.IMREAD_GRAYSCALE)

        padding.insert(0, (0, 0))
        image_pad = np.pad(image, padding)

        return image_pad

    def create_items(self, fragment, mask_pad):
        items = []
        overlap_size = int(self.overlap * self.tile_size)
        x_list = np.arange(0, mask_pad.shape[1] - overlap_size, overlap_size).tolist()
        y_list = np.arange(0, mask_pad.shape[0] - overlap_size, overlap_size).tolist()

        for x in x_list:
            for y in y_list:
                bbox = torch.IntTensor([x, y, x + self.tile_size, y + self.tile_size])
                x0, y0, x1, y1 = bbox
                tile = mask_pad[y0:y1, x0:x1]

                if tile.sum() / (255 * self.tile_size ** 2) >= self.selection_thr:
                    items.append({'fragment': fragment, 'bbox': bbox})

        return items

    def make_data(self):
        data = {}
        items = []

        for fragment in self.fragments:
            fragment_path = os.path.join(self.set_path, str(fragment))
            mask_pad, shape, padding = self.make_mask(fragment_path)
            image_pad = self.make_image(fragment_path, shape, padding)
            items += self.create_items(fragment, mask_pad)

            data[fragment] = {
                'mask': torch.from_numpy(mask_pad).to(self.device),
                'image': torch.from_numpy(image_pad).to(self.device)
            }

        return data, items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        fragment, bbox = self.items[idx]['fragment'], self.items[idx]['bbox']
        x0, y0, x1, y1 = bbox

        mask = torch.unsqueeze(self.data[fragment]['mask'][y0:y1, x0:x1] / 255.0, dim=0)
        image = self.data[fragment]['image'][:, y0:y1, x0:x1] / 255.0

        if self.augmentation:
            seed = random.randint(0, 2 ** 32)
            torch.manual_seed(seed)
            image = self.transforms(image)
            torch.manual_seed(seed)
            mask = self.transforms(mask)

        return fragment, bbox, mask, image
