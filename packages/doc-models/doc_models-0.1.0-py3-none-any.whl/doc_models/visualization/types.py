from dataclasses import dataclass, field

import cv2
import numpy as np
from doc_models.components.page import Page
from doc_models.types import BBox


class TextBox(BBox):
    def __init__(
        self,
        text: str,
        left: float = None,
        right: float = None,
        top: float = None,
        bottom: float = None,
        width: float = None,
        height: float = None,
        line_space: float = None,
    ):
        self.text = text
        self.line_space = line_space
        super().__init__(left, right, top, bottom, width, height)


@dataclass
class Font:
    # The font type:
    # FONT_HERSHEY_SIMPLEX (normal size sans-serif font)
    # FONT_HERSHEY_PLAIN (small size sans-serif font)
    # FONT_HERSHEY_DUPLEX (normal size sans-serif font. more complex than FONT_HERSHEY_SIMPLEX)
    font_face: int = cv2.FONT_HERSHEY_DUPLEX
    # Font scale factor that is multiplied by the font-specific base size.
    font_scale: float = 1
    # The thickness of the line in px.
    thickness: int = 2
    # The type of line:
    # FILLED
    # LINE_4 (4-connected line)
    # LINE_8 (8-connected line)
    # LINE_AA (antialiased line)
    line_type: int = cv2.LINE_8


@dataclass
class PageImg:
    img: np.ndarray = None
    page: Page = None
    ft_names: set = field(default_factory=set)
