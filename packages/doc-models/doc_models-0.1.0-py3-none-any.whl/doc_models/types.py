"""Common data types."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, NewType, Sequence, Union

from poppler.document import Document

PopDoc = NewType("PopDoc", Document)
OCREngine = Literal["tesseract"]
FilePath = Union[str, Path]


class WriteOnceDict(dict):
    """A dictionary that only allows the addition of new unique keys."""

    def __setattr__(self, key, value):
        raise AttributeError("Setting attributes is not allowed")

    def __delitem__(self, key):
        raise KeyError("Read-only dictionary")

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"{key} has already been set")
        dict.__setitem__(self, key, value)


@dataclass
class Point2d:
    """A point in 2d space."""

    x: int
    y: int


class BBox:
    """A bounding box with integer dimensions."""

    def __init__(
        self,
        left: float = None,
        right: float = None,
        top: float = None,
        bottom: float = None,
        width: float = None,
        height: float = None,
    ):
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom
        self._width = width
        self._height = height

        self.update()

    @classmethod
    def from_bboxes(cls, bboxes: Sequence["bbox"]):
        """Create a bbox enclosing the argument bboxes.

        Args:
            bboxes (Sequence["bbox"]): Bounding boxes.
        """
        return cls(
            left=min(b.left for b in bboxes),
            right=max(b.right for b in bboxes),
            top=min(b.top for b in bboxes),
            bottom=max(b.bottom for b in bboxes),
        )

    def update(self, **kwargs):
        attrs = ("top", "left", "bottom", "right", "width", "height")
        if kwargs:
            # update attributes.
            for a in attrs:
                if a in kwargs:
                    setattr(self, f"_{a}", kwargs[a])
        if self.is_valid:
            # precompute dependant attributes.
            for a in attrs:
                setattr(self, f"_{a}", getattr(self, a))

    @property
    def is_valid(self) -> bool:
        """Return True if enough attributes are set for all the properties to resolve.
        If there is not, accessing certain properties will result in indefinite recursion error.
        """
        return (
            len([v for v in (self._top, self._bottom, self._height) if v is not None])
            >= 2
            and len(
                [v for v in (self._left, self._right, self._width) if v is not None]
            )
            >= 2
        )

    @property
    def top(self) -> int:
        return self._top if self._top is not None else self.bottom - self.height

    @property
    def left(self) -> int:
        return self._left if self._left is not None else self.right - self.width

    @property
    def right(self) -> int:
        return self._right if self._right is not None else self.left + self.width

    @property
    def bottom(self) -> int:
        return self._bottom if self._bottom is not None else self.top + self.height

    @property
    def width(self) -> int:
        return self._width or self.right - self.left

    @property
    def height(self) -> int:
        return self._height or self.bottom - self.top

    @property
    def x_center(self) -> int:
        """Half way between bounding box left and right"""
        return self.left + self.width / 2

    @property
    def y_center(self) -> int:
        """Half way between bounding box top and bottom (in page coordinates)"""
        return self.top + self.height / 2

    @property
    def top_center(self) -> Point2d:
        return Point2d(self.x_center, self.top)

    @property
    def bottom_center(self) -> Point2d:
        return Point2d(self.x_center, self.bottom)

    @property
    def left_center(self) -> Point2d:
        return Point2d(self.left, self.y_center)

    @property
    def right_center(self) -> Point2d:
        return Point2d(self.right, self.y_center)

    @staticmethod
    def fraction_overlap(b1: "bbox", b2: "bbox") -> float:
        """Get fraction overlap of two bbox"""
        if b1.left >= b2.right:
            # b1 starts after b2 ends.
            return 0.0
        if b1.right <= b2.left:
            # b1 ends before b2 starts.
            return 0.0
        left_end_gap = 0.0
        # left end of page is 0, right end is 1.
        if b1.left < b2.left:
            # left of b1 extends beyond b2 left.
            left_end_gap = b2.left - b1.left
        right_end_gap = 0.0
        if b1.right > b2.right:
            # right of b1 extends beyond b2 right.
            right_end_gap = b1.right - b2.right
        b1_width = b1.right - b1.left
        return (b1_width - right_end_gap - left_end_gap) / b1_width

    def __repr__(self):
        return f"BBox(left={self.left}, right={self.right}, top={self.top}, bottom={self.bottom})"
