from dataclasses import dataclass, field
from typing import List, Sequence

from doc_models.clustering.spacing import DocLineSpacing
from doc_models.clustering.vertical import vertical_line_clusters
from doc_models.components.cluster import Cluster
from doc_models.components.word import Word
from doc_models.types import BBox


def load_page_line_words(words: Sequence[Word]) -> Sequence[List[Word]]:
    """Load a list of all words on page into list of lines.

    A Line contains Words that have the same vertical position on the page
    (i.e. a normal reading line).
    """
    lines = []
    if words:
        # sort words by bottom position (smallest to largest).
        words.sort(key=lambda w: w.bbox.bottom)
        line_words = []
        for next_idx, word in enumerate(words[:-1], start=1):
            # add word to group.
            line_words.append(word)
            if words[next_idx].bbox.bottom - word.bbox.bottom > 1:
                # line has ended. get line segments.
                lines.append(line_words)
                line_words = []
        # add last word to last line.
        line_words.append(words[-1])
        lines.append(line_words)
    # sort line words left to right (reading order)
    for line_words in lines:
        line_words.sort(key=lambda w: w.bbox.left)
    return lines


@dataclass
class Page:
    """A PDF page."""

    index: int
    bbox: BBox
    lines: List[Cluster]
    line_clusters: List[Cluster] = field(default_factory=list)
    clusters: List[Cluster] = field(default_factory=list)

    def set_clusters(self, line_spacing: DocLineSpacing):
        """Compute and set the cluster attribute."""
        self.line_clusters = vertical_line_clusters(self, line_spacing)
