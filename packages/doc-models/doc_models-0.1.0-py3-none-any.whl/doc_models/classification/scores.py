

from doc_models.components.cluster import Cluster
from doc_models.utils import coef_of_var


class Scorer:
    """Record weighted score components and compute a resulting score."""

    def __init__(self) -> None:
        self._weighted_score_sum = 0
        self._weight_sum = 0

    @property
    def score(self) -> float:
        """The net resulting score."""
        return self._weight_sum / self._weighted_score_sum

    def add_component(self, value: float, max_possible: float, weight: float = 1):
        """Add a component to the net score."""
        self._weighted_score_sum += weight * (value / max_possible)
        self._weight_sum += weight


def text_similarity(c1: Cluster, t2: Cluster) -> float:
    """Get a number 0-1 that shows how similar word space is. (1 being exactly the same)

    Args:
        c1: A line or cluster.
        t2: A line or cluster.
    """

    smaller, larger = sorted([t2.avg_word_space, c1.avg_word_space])
    scorer = Scorer()
    # add 2 if word space size is similar.
    scorer.add_component(
        value=2 - 2 * (smaller / larger) if larger != 0 else 0, max_possible=2
    )
    # add 1 if amount of bold words is the same.
    scorer.add_component(value=1 - abs(c1.bold_ratio - t2.bold_ratio), max_possible=1)
    # add 1 if capitalized or uppercase is the same.
    scorer.add_component(
        value=1
        - max(
            abs(c1.capitalized_ratio - t2.capitalized_ratio),
            abs(c1.uppercase_ratio - t2.uppercase_ratio),
        ),
        max_possible=1,
    )
    # add 2 if word spaces are the same.
    scorer.add_component(
        value=2 - 2 * max(1, abs(c1.word_space_cov - t2.word_space_cov)),
        max_possible=2,
    )
    return scorer.score


def line_paragraph_score(line: Cluster) -> float:
    scorer = Scorer()
    # normal paragraph lines should have words with consistent single space.
    scorer.add_component(value=1 - line.word_space_cov, max_possible=1)
    # increase score for not repeatedly changing font size.
    scorer.add_component(value=max(0, 1 - line.font_size_cov), max_possible=1)
    # increase score for not repeatedly changing font name.
    scorer.add_component(
        value=max(0, 1 - line.font_name_changes / (line.word_count - 1)), max_possible=1
    )

    # paragraph line should start close to page left.
    scorer.add_component(value=max(0, 1 - 2.15 * line.left_skew), max_possible=1)
    # paragraph line should end close to page right.
    scorer.add_component(value=max(0, 1 - 2.15 * line.right_skew), max_possible=1)
    # a paragraph line should have at least 5 words.
    scorer.add_component(value=1 if line.word_count >= 5 else 0, max_possible=1)
    # increase score for containing a sentence end/start.
    scorer.add_component(value=0.5 if line.sentences > 0 else 0, max_possible=0.5)
    return scorer.score


def cluster_paragraph_score(cluster: Cluster) -> float:
    """Check if cluster is typical paragraph text. Small number mean typical paragraph text."""
    scorer = Scorer()
    lines = cluster.members
    # check if lines have a similar average font size.
    scorer.add_component(
        value=coef_of_var([line.avg_font_size for line in lines]), max_possible=1
    )
    # check if lines use similar font.
    scorer.add_component(
        value=len({l.dominant_font_name for l in lines}) / len(lines), max_possible=1
    )
    # check if left skew is similar.
    scorer.add_component(
        value=coef_of_var([l.left_skew for l in lines]), max_possible=1
    )
    # check if right skew is approx similar.
    scorer.add_component(
        value=coef_of_var([l.right_skew for l in lines]), max_possible=1
    )
    # check if average word space is similar.
    scorer.add_component(
        value=coef_of_var([l.word_space_cov for l in lines]), max_possible=1
    )
    # check if lines have similar word count.
    scorer.add_component(
        value=coef_of_var([l.word_count for l in lines]), max_possible=1
    )
    return scorer.score
