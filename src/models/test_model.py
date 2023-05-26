import os
import sys

sys.path.insert(1, os.path.abspath(os.path.curdir))

from src.utils import get_device
from torch.utils.data import DataLoader
from src.data.make_dataset import DatasetVesuvius
from constant import TRAIN_FRAGMENTS, TILE_SIZE, Z_DIM
from unet3d import Unet3d

device = get_device()

model = Unet3d(list_channels=[1, 32, 64], inputs_size=TILE_SIZE).half().to(device)

train_dataset = DatasetVesuvius(fragments=TRAIN_FRAGMENTS,
                                tile_size=TILE_SIZE,
                                num_slices=Z_DIM,
                                random_slices=False,
                                selection_thr=0.01,
                                augmentation=True,
                                test=False,
                                device=device)

train_dataloader = DataLoader(dataset=train_dataset,
                              batch_size=16)

for fragment, bbox, mask, image in train_dataloader:
    print(train_dataset.slices)
    print(fragment)
    print(bbox.shape)
    print(mask.shape)
    print(image.shape)

    res = model(image)
    print(res.shape)
    break


