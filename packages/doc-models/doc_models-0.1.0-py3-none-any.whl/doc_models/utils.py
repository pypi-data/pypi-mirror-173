"""Common utility functions."""

from statistics import mean, stdev
from typing import Any, Dict, List, Sequence

import numpy as np
from ready_logger import get_logger

from .types import BBox

logger = get_logger("pdf-extract")


def singleton(cls):
    """Used as a decorator, this will cause the class definition to be an instance of ``cls`` at runtime rather than
    the actual class definition.

    Args:
        cls: The class that is being decorated.

    Returns:
        An instance of ``cls``

    """
    return cls()


def pdf_bbox_to_img(pdf_bbox: BBox, img: np.array) -> BBox:
    """Convert bounding box coordinates in PDF space to coordinates in image space.

    Args:
        pdf_bbox (BBox): Bounding box in PDF coordinates.
        img (np.array): Image that bounding box should be scaled to.

    Returns:
        BBox: Bounding box with image coordinates.
    """
    img_height, img_width, _ = img.shape
    width_scalar = img_width / pdf_bbox.width
    height_scalar = img_height / pdf_bbox.height
    return BBox(
        left=round(width_scalar * pdf_bbox.left),
        right=round(width_scalar * pdf_bbox.right),
        top=round(height_scalar * pdf_bbox.top),
        bottom=round(height_scalar * pdf_bbox.bottom),
    )


def img_bbox_to_pdf(img_bbox: BBox, pdf_page: "Page") -> BBox:
    """Convert bounding box coordinates in image space to coordinates in PDF space.

    Args:
        img_bbox (BBox): Bounding box in image coordinates.
        pdf_page (Page): Page that bounding box should be scaled to.

    Returns:
        BBox: Bounding box in PDF coordinates.
    """
    width_scalar = pdf_page.bbox.width / img_bbox.width
    height_scalar = pdf_page.bbox.height / img_bbox.height
    return BBox(
        left=round(width_scalar * img_bbox.left),
        right=round(width_scalar * img_bbox.right),
        top=round(height_scalar * img_bbox.top),
        bottom=round(height_scalar * img_bbox.bottom),
    )


def val_closest_key(search_in: Dict[float, Any], search_key: float) -> Any:
    """Find key in dictionary that is closest to the provided value and return the value at that key.

    Args:
        search_in (Dict[float, Any]): The dictionary to search in.
        search_key (float): The value that should be searched for.

    Returns:
        Any: Value at matched key.
    """
    if search_key in search_in:
        return search_in[search_key]
    return search_in[min(search_in.keys(), key=lambda k: abs(k - search_key))]


def fraction_different(n1: float, n2: float) -> float:
    """Compute the fraction difference of two values.

    Args:
        n1 (float): Some value.
        n2 (float): Some value.

    Returns:
        float: The fraction difference.
    """
    denominator = n1 + n2
    if denominator:
        return (n1 - n2) / (denominator * 0.5)
    return 0.0


def coef_of_var(values: Sequence[float]) -> float:
    """Compute the coefficient of variation of a list of values."""
    if values is not None and len(values) > 1:
        return stdev(values) / mean(values)
    return 0.0


def iqr_truncate(values: Sequence[float]) -> List[float]:
    """Truncate a range of values using interquartile range.

    Args:
        values (Sequence[float]): The values to truncate.

    Returns:
        List[float]: The truncated values
    """
    q1, q3 = np.percentile([v for v in values if v is not None], [25, 75])
    iqr = q3 - q1
    upper_bound = q3 + (1.5 * iqr)
    lower_bound = q1 - (1.5 * iqr)
    return [min(max(v, lower_bound), upper_bound) for v in values]


def truncate_normalize(l: List[Any]):
    tmp = [v for v in l if v is not None]
    if not len(tmp):
        return l
    # truncate outliers to min/max non-outlier values
    tmp = iqr_truncate(tmp)
    # normalize
    _min, _max = min(tmp), max(tmp)
    if _min == _max or _min > 0:
        if _max == 0:
            return l
        return [v / _max if v is not None else None for v in l]
    return [(v - _min) / (_max - _min) if v is not None else None for v in l]
