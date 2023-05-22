import os, sys
sys.path.insert(0, os.pardir)

from typing import List, Dict
import torch

from constant import TILE_SIZE, TRAIN_FRAGMENTS_PATH, TEST_FRAGMENTS_PATH


def reconstruct_images(
    sub_masks: torch.Tensor,
    bboxs: torch.Tensor,
    fragment_ids: List,
    mask_shapes: Dict,
):
    # Implementation of the reconstruction logic
    # Combine sub-masks to reconstruct the original images separately
    # Handle overlap by taking the mean of overlapping pixels

    reconstructed_images = {
        fragment_id: torch.zeros(mask_size).to(device=sub_masks.device)
        for fragment_id, mask_size in mask_shapes.items()
    }
    count_map = {
        fragment_id: torch.zeros(mask_size).to(device=sub_masks.device)
        for fragment_id, mask_size in mask_shapes.items()
    }

    for i in range(sub_masks.shape[0]):
        reconstructed_images[fragment_ids[i]][
            bboxs[i, 0] : bboxs[i, 2], bboxs[i, 1] : bboxs[i, 3]
        ] += sub_masks[i, :, :]
        count_map[fragment_ids[i]][
            bboxs[i, 0] : bboxs[i, 2], bboxs[i, 1] : bboxs[i, 3]
        ] += 1

    # Divide by the count map to obtain the mean value
    for key in mask_shapes.keys():
        reconstructed_images[key] /= count_map[key]
        reconstructed_images[key] = torch.nan_to_num(reconstructed_images[key], nan=0)

    return reconstructed_images


def get_mask_shape():
    return TILE_SIZE, TILE_SIZE


def get_dict_mask_shapes(list_fragment_ids):
    return {fragment_id: get_mask_shape() for fragment_id in list_fragment_ids}


def get_device():
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    return torch.device(device=device)
