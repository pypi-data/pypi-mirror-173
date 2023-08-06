# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Unit tests for augmentation for object detection."""

import os
import pytest

import torch

from PIL import Image

from azureml.automl.dnn.vision.object_detection.common.augmentations import transform


@pytest.mark.usefixtures("new_clean_dir")
@pytest.mark.parametrize("is_train", [False, True])
def test_transform(is_train):
    image_root = "object_detection_data/images"
    image = Image.open(os.path.join(image_root, "000001030.png")).convert("RGB")
    height, width = image.height, image.width
    image_area = width * height
    boxes = torch.Tensor([
        [int(0.25 * width), int(0.25 * height), int(0.5 * width), int(0.5 * height)],
        [int(0.5 * width), int(0.5 * height), int(0.75 * width), int(0.75 * height)],
    ])

    for _ in range(100):
        new_image, new_boxes, new_areas, new_height, new_width, _ = transform(image, boxes, is_train, 0.5)

        assert new_image.shape[1] == new_height
        assert new_image.shape[2] == new_width
        assert (new_height >= 0.5 * image.height) and (new_height <= 2 * image.height)
        assert (new_width >= 0.5 * image.width) and (new_width <= 2 * image.width)

        assert (new_areas[0] >= 0.0625 * image_area) and (new_areas[0] <= 0.25 * image_area)
        assert (new_areas[1] >= 0.0625 * image_area) and (new_areas[1] <= 0.25 * image_area)
        assert len(new_boxes) == 2


@pytest.mark.usefixtures("new_clean_dir")
def test_transform_empty_boxes():
    image_root = "object_detection_data/images"
    image = Image.open(os.path.join(image_root, "000001030.png")).convert("RGB")

    _, new_boxes, new_areas, _, _, _ = transform(image, torch.Tensor([]), False, 0.5)

    assert len(new_boxes) == 0
    assert len(new_areas) == 0
