from collections import Counter
from typing import Optional, Sequence, Union

from doc_models.clustering.spacing import DocWordSpacing
from doc_models.types import BBox
from doc_models.utils import coef_of_var

from .line_segment import LineSegment
from .word import Word


class Cluster:
    def __init__(
        self,
        members: Sequence[Union[LineSegment, "Cluster"]],
        page_bbox: BBox,
        y_index: Optional[int] = None,
        x_index: Optional[int] = None,
    ):
        self.members = members
        self.y_index = y_index
        self.x_index = x_index
        self.words = []
        self.word_font_sizes = []
        self.word_spaces = []
        for m in members:
            self.words += m.words
            self.word_font_sizes += m.word_font_sizes
            self.word_spaces += m.word_spaces

        self.bbox = BBox.from_bboxes([m.bbox for m in members])
        self.word_count = sum(s.word_count for s in members)
        self.text = " ".join([m.text for m in members])
        self.font_name_changes = sum(m.font_name_changes for m in members)
        self.dominant_font_name = max(
            Counter([w.font_name for w in self.words]).items(), key=lambda w: w[1]
        )[0]
        self.font_size_cov = coef_of_var(self.word_font_sizes)
        self.bold_ratio = (
            sum(m.bold_ratio * m.word_count for m in members) / self.word_count
        )
        self.italic_ratio = (
            sum(m.italic_ratio * m.word_count for m in members) / self.word_count
        )
        self.capitalized_ratio = (
            sum(m.capitalized_ratio * m.word_count for m in members) / self.word_count
        )
        self.uppercase_ratio = (
            sum(m.uppercase_ratio * m.word_count for m in members) / self.word_count
        )
        self.word_space_cov = coef_of_var(self.word_spaces)
        self.avg_word_space = (
            sum(m.avg_word_space * m.word_count for m in members) / self.word_count
        )
        self.avg_font_size = (
            sum(m.avg_font_size * m.word_count for m in members) / self.word_count
        )
        self.sentence_count = sum(m.sentence_count for m in members)
        self.is_underline = all(m.is_underline for m in members)
        # Fraction of page width line end deviates from page right.
        self.page_right_skew = (page_bbox.right - self.bbox.right) / page_bbox.width
        # Fraction of page width line end deviates from page left.
        self.page_left_skew = (self.bbox.left - page_bbox.left) / page_bbox.width
        # assigned after all lines are constructed.
        self.whitespace_above = None
        self.whitespace_below = None

    @classmethod
    def from_line_words(
        cls,
        words: Sequence[Word],
        exp_word_space: DocWordSpacing,
        page_bbox: BBox,
        is_sorted: bool = False,
    ):
        """Create a cluster that represents a line. The members are line segments."""
        words = sorted(words, key=lambda w: w.bbox.left) if not is_sorted else words
        segments = []
        segment_words = [words[0]]
        for word in words[1:]:
            # check if actual word space is approximately expected word space.
            if exp_word_space.is_expected_word_space(segment_words[-1], word):
                # word should be member of segment.
                segment_words.append(word)
            else:
                # word space not expected, so segment is finished.
                segments.append(LineSegment(segment_words, is_sorted=True))
                segment_words = [word]
        segments.append(LineSegment(segment_words))
        return cls(segments, page_bbox)

    @staticmethod
    def set_vertical_whitespace(clusters: Sequence["Cluster"]):
        """Set whitespace above and below each Cluster. Clusters should be sorted vertically."""
        for next_idx, upper in enumerate(clusters[:-1], start=1):
            lower = clusters[next_idx]
            whitespace = max(0, lower.bbox.top - upper.bbox.bottom)
            upper.whitespace_below = whitespace
            lower.whitespace_above = whitespace
        clusters[-1].whitespace_below = 0.0

    def __repr__(self) -> str:
        return f"Cluster(x_index={self.x_index}, y_index={self.y_index}, {self.bbox})"
