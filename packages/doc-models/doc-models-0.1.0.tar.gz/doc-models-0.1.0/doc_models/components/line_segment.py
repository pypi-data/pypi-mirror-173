import re
from collections import Counter
from statistics import mean
from typing import Sequence

from doc_models.types import BBox
from doc_models.utils import coef_of_var

from .word import Word


class LineSegment:
    """A grouping of colinear words with expected word spacing."""

    _sentence_count_re = re.compile(r"\w[.?!](\s|$)")
    _is_underline_re = re.compile(r"^_+$")

    def __init__(self, words: Sequence[Word], is_sorted: bool = False):
        """
        Args:
            words (Sequence[Word]): Words composing the line segment.
            is_sorted (bool, optional): True if words are sorted left to right. Defaults to False.
        """
        # sort line words left to right (reading order)
        self.words = (
            sorted(words, key=lambda w: w.bbox.left) if not is_sorted else words
        )
        self.bbox = BBox(
            left=self.words[0].bbox.left,
            right=self.words[-1].bbox.right,
            top=min(w.bbox.top for w in self.words),
            bottom=max(w.bbox.bottom for w in self.words),
        )
        self.word_count = len(self.words)
        self.text = " ".join([w.text for w in self.words])
        self.word_font_sizes = [w.font_size for w in self.words]
        self.word_spaces = [
            self.words[next_idx].bbox.left - word.bbox.right
            for next_idx, word in enumerate(self.words[:-1], start=1)
        ]
        self.font_name_changes = sum(
            1
            for next_idx, word in enumerate(self.words[:-1], start=1)
            if self.words[next_idx].font_name != word.font_name
        )
        self.dominant_font_name = max(
            Counter([w.font_name for w in self.words]).items(), key=lambda w: w[1]
        )[0]
        self.avg_font_size = mean(self.word_font_sizes)

        self.font_size_cov = coef_of_var(self.word_font_sizes)
        self.bold_ratio = len([w for w in self.words if w.is_bold]) / self.word_count
        self.italic_ratio = (
            len([w for w in self.words if w.is_italic]) / self.word_count
        )
        self.capitalized_ratio = (
            len([w for w in self.words if w.is_capitalized]) / self.word_count
        )
        self.uppercase_ratio = (
            len([w for w in self.words if w.is_uppercase]) / self.word_count
        )
        self.word_space_cov = coef_of_var(self.word_spaces)
        self.avg_word_space = mean(self.word_spaces) if len(self.word_spaces) > 1 else 0
        self.sentence_count = len(self._sentence_count_re.findall(self.text))
        self.is_underline = bool(self._is_underline_re.match(self.text))
        # assigned after all lines are constructed.
        self.whitespace_above = None
        self.whitespace_below = None

    def __repr__(self):
        return f"LineSegment('{self.text}', {self.bbox})"
