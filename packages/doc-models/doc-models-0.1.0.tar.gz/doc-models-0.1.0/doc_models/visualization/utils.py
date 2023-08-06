import re
from typing import Literal, Union

import numpy as np

from .types import PageImg


def pad_image(
    img: np.array,
    padding_size: int,
    padding_dir: Literal["left", "right", "top", "bottom"],
) -> None:
    """Add white padding to image.

    Args:
        img (np.array): _description_
        padding_size (int): _description_
        padding_dir (Literal[&quot;left&quot;, &quot;right&quot;]): _description_

    Raises:
        ValueError: _description_
    """
    height, _, channels = img.shape
    padding = np.full(
        (height, padding_size, channels),
        (255, 255, 255),
        dtype=np.uint8,
    )
    if padding_dir == "left":
        img = np.concatenate([padding, img], axis=1)
    elif padding_dir == "right":
        img = np.concatenate([img, padding], axis=1)
    elif padding_dir == "top":
        img = np.concatenate([padding, img], axis=0)
    elif padding_dir == "bottom":
        img = np.concatenate([img, padding], axis=0)
    else:
        raise ValueError(f"Invalid padding direction: {padding_dir}")


def round_if_float(value: Union[str, float]) -> str:
    """Round float value and convert to string"""
    if isinstance(value, str) and (match := re.search(r"\d+\.\d+", value)):
        value = float(match.group())
    if isinstance(value, float):
        value = round(value, 3)
    return str(value)
