from itertools import cycle
from random import randint
from typing import Tuple

from doc_models.utils import singleton

Color = Tuple[int, int, int]


@singleton
class BGRColors:
    """BGR color tuples"""

    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    PURPLE = (127, 0, 127)
    YELLOW = (0, 255, 255)
    ORANGE = (0, 127, 255)


# create cyclic iterator of random colors.
bgr_color_iter = cycle(
    [
        (245, 66, 66),
        (245, 138, 66),
        (245, 203, 66),
        (200, 245, 66),
        (126, 245, 66),
        (66, 245, 221),
        (66, 164, 245),
        (75, 66, 245),
        (132, 66, 245),
        (197, 66, 245),
        (245, 66, 245),
        (245, 66, 144),
        (245, 66, 102),
    ]
)


def next_color() -> Tuple[int, int, int]:
    return next(bgr_color_iter)


def random_color() -> Tuple[int, int, int]:
    """Generate a random tuple of values for b,g,r or r,g,b."""
    return (randint(100, 255), randint(100, 255), randint(100, 255))
