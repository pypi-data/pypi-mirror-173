from collections import defaultdict
from pprint import pformat
from typing import Dict, List, Sequence, Set

from doc_models import const, logger
from doc_models.components.word import Word
from doc_models.types import BBox
from doc_models.utils import fraction_different


class DocWordSpacing:
    """Utility class for making inferences about word spacing using data aggregated from all document pages."""

    def __init__(self, lines: Sequence[Sequence[Word]]):
        self._font_size_space_indexes = self._get_font_size_space_indexes(lines)
        # get common word spaces for each font size.
        self._font_size_common_word_spaces = _font_common_spaces(
            self._font_size_space_indexes,
            const.MIN_WORD_SPACE_COUNT_RATIO,
        )
        self.font_size_space_clusters = self._font_size_space_clusters()

    def is_expected_word_space(self, left_word: Word, right_word: Word) -> bool:
        """Check if space between left_word and right_word is approximately as expected.

        Args:
            left_word (Word): The colinear word preceding `right_word`
            right_word (Word): The colinear word proceeding `left_word`

        Returns:
            bool: True if space between words is the expected space.
        """

        if self.is_common_word_space(left_word, right_word):
            return True
        # check if word is a member of a cluster of consecutive words with same font size + same word space.
        return left_word.index in self.font_size_space_clusters.get(
            left_word.font_size, []
        )

    def is_common_word_space(self, left_word: Word, right_word: Word) -> bool:
        """Check if space between words is a common space for the font size

        Args:
            left_word (Word): The colinear word preceding `right_word`
            right_word (Word): The colinear word proceeding `left_word`

        Returns:
            bool: True if space between words is a common space for the font size
        """

        space = right_word.bbox.left - left_word.bbox.right
        for font_size in {left_word.font_size, right_word.font_size}:
            # TODO use space, space count in _font_size_common_word_spaces and weight by count.
            for common_space in self._font_size_common_word_spaces.get(font_size, []):
                if (
                    abs(space - common_space) / common_space
                    < const.MAX_COMMON_WORD_SPACE_DIFF
                ):
                    return True
        return False

    def _font_size_space_clusters(self) -> Dict[str, Set[int]]:
        """Find ranges of consecutive words with at least 3 with words with same font size and same space.

        Returns:
            Dict[str, Set[int]]: Map font size to set of all word indexes that are members of a cluster of consecutive words with same font size + same word space.
        """
        font_cluster_indexes = {}
        for font_size, space_to_space_indexes in self._font_size_space_indexes.items():
            cluster_indexes = []
            for space_indexes in space_to_space_indexes.values():
                try:
                    space_indexes = iter(space_indexes)
                    space_index = next(space_indexes)
                    while True:
                        # 3 words = 2 consecutive space indexes, so check current and next.
                        if (next_space_index := next(space_indexes)) == space_index + 1:
                            cluster_indexes.append(space_index)
                            cluster_indexes.append(next_space_index)
                            while (next_space_index := next(space_indexes)) == (
                                cluster_indexes[-1] + 1
                            ):
                                cluster_indexes.append(next_space_index)
                        space_index = next_space_index
                except StopIteration:
                    pass
            font_cluster_indexes[font_size] = set(cluster_indexes)
        return font_cluster_indexes

    def _get_font_size_space_indexes(
        self,
        lines: Sequence[Sequence[Word]],
        rounding_precision: int = 1,
    ) -> Dict[float, Dict[float, List[int]]]:
        """Get map of font size to map of word proceeding whitespace occurrence indexes."""
        font_size_space_indexes = defaultdict(lambda: defaultdict(list))
        for line in lines:
            for next_index, word in enumerate(line[:-1], start=1):
                next_word = line[next_index]
                # only use if font size is the same for both words.
                if word.font_size == next_word.font_size:
                    # get the amount of whitespace between two words.
                    # TODO determine rounding precision based on page width.
                    word_space = round(
                        next_word.bbox.left - word.bbox.right, rounding_precision
                    )
                    font_size_space_indexes[word.font_size][word_space].append(
                        word.index
                    )
        return font_size_space_indexes


class DocLineSpacing:
    def __init__(self, pages: List["Page"]):
        self.pages = pages
        self._font_line_spaces_indexes = self._get_font_line_spaces_indexes()
        # take weighted average of most frequently occurring line spaces for each font size that occurs at least decently frequently.
        self._font_size_common_line_spaces = _font_common_spaces(
            self._font_line_spaces_indexes,
            min_space_count_ratio=const.MIN_LINE_SPACE_COUNT_RATIO,
        )

    def is_expected_line_space(
        self,
        upper_line: "Cluster",
        lower_line: "Cluster",
    ) -> bool:
        """Return True if whitespace between two lines is approximately as expected.

        Calculation is based off of line's average font size and can only be calculated if
        document has a sufficient number of lines with this font size.
        """
        avg_font_size = self._lines_avg_font_size(upper_line, lower_line)
        if avg_font_size not in self._font_size_common_line_spaces:
            return False
        line_spacings = self._font_size_common_line_spaces[avg_font_size]
        # space between lines = whitespace below first line = whitespace above seconds line
        space = upper_line.whitespace_below
        for exp_space in line_spacings:
            # approximation to eliminate division by 0 problems.
            if exp_space == 0:
                exp_space = 0.01
            if abs(space - exp_space) / exp_space < const.MAX_COMMON_LINE_SPACE_DIFF:
                return True

    def _get_font_line_spaces_indexes(self) -> Dict[float, Dict[float, List[int]]]:
        """Get map of line font size to map of vertical whitespace occurrence indexes."""
        font_line_spaces_indexes = defaultdict(lambda: defaultdict(list))
        for page in self.pages:
            for next_index, line in enumerate(page.lines[:-1], start=1):
                next_line = page.lines[next_index]
                # Check that lines have font sizes that are approximately the same and also have some horizontal overlap.
                if (
                    BBox.fraction_overlap(line.bbox, next_line.bbox) > 0.5
                    and abs(
                        fraction_different(line.avg_font_size, next_line.avg_font_size)
                    )
                    < 0.2
                ):
                    font_size = self._lines_avg_font_size(line, next_line)
                    # Get the vertical whitespace between two lines.
                    # TODO determine rounding precision based on page height.
                    font_line_spaces_indexes[font_size][
                        round(line.whitespace_below, 1)
                    ].append(line.y_index)
        return font_line_spaces_indexes

    def _lines_avg_font_size(
        self, upper_line: "Cluster", lower_line: "Cluster"
    ) -> float:
        """Get the average font size of lines."""
        return round(
            (upper_line.avg_font_size + lower_line.avg_font_size) / 2,
            const.FONT_ROUNDING_PRECISION,
        )


def _font_common_spaces(
    font_size_space_indexes: Dict[float, Dict[float, List[int]]],
    min_space_count_ratio: float,
    min_space_count: int = 3,
) -> Dict[float, Set[float]]:
    """Find common space sizes for each font size.

    Args:
        font_size_space_indexes: map font size to indexes.
        min_space_count_ratio: minimum allowable ratio of space count / max space count for each font size. (used for filtering)
    """
    # filter each key's values based on max weight ratio for that specific key.
    font_common_spaces = {}
    for font_size, space_indexes in font_size_space_indexes.items():
        space_counts = {space: len(indexes) for space, indexes in space_indexes.items()}
        if space_counts:
            max_space_count = max(list(space_counts.values()))
            if spaces := {
                space
                for space, count in space_counts.items()
                if count > min_space_count
                and count / max_space_count > min_space_count_ratio
            }:
                font_common_spaces[font_size] = spaces

    logger.debug(
        "Font common spaces (filtered by min space count ratio of %s): %s",
        min_space_count_ratio,
        pformat(font_common_spaces),
    )
    return font_common_spaces
