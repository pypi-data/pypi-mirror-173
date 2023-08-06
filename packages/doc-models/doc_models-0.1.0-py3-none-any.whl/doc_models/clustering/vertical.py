from statistics import mean
from typing import List

from doc_models.classification.scores import text_similarity
from doc_models.clustering.spacing import DocLineSpacing
from doc_models.components.cluster import Cluster
from doc_models.utils import fraction_different


def vertical_line_clusters(page: "Page", line_spacing: DocLineSpacing) -> List[Cluster]:
    """Find clusters of lines with same vertical spacing.

    Args:
        page (Page): Page with lines that should be clustered.
        line_spacing (DocLineSpacing): Document line spacing.

    Returns:
        List[Cluster]: vertical line clusters.
    """
    vertical_clusters = []

    def _check_and_add(cluster: Cluster):
        """Resolve boundary conflicts and add cluster if it is still a valid cluster after conflict resolution."""
        if not vertical_clusters:
            # this is the first cluster. no boundary conflicts to resolve.
            vertical_clusters.append(cluster)
            return
        prev_cluster = vertical_clusters[-1]
        # this will be different if previous cluster candidate (arg to previous call to _check_and_add) was not added.
        # if it was added, this line will currently be shared between the two clusters (last line in prev cluster and first line in current cluster)
        if (common_line := cluster.members[0]) != prev_cluster.members[-1]:
            # no boundary conflicts. add current cluster.
            vertical_clusters.append(cluster)
            return
        # use text similarity to find cluster that line is more similar to.
        # if text similarity is the same, assign the line to the larger cluster.
        cc_sim = text_similarity(common_line, cluster)
        pc_sim = text_similarity(common_line, prev_cluster)
        if (
            cc_sim > pc_sim
            or cc_sim == pc_sim
            and len(cluster.members) > len(prev_cluster.members)
        ):
            if len(prev_cluster.members) > 2:
                # common line is more similar to current cluster, so remove it from previous cluster.
                vertical_clusters[-1] = Cluster(
                    members=prev_cluster.members[:-1], page_bbox=page.bbox
                )
            else:
                # this will no longer be a valid cluster if we remove a line, so delete the cluster.
                del vertical_clusters[-1]
            # add current cluster.
            vertical_clusters.append(cluster)
        elif len(cluster.members) > 2:
            # common line is more similar to previous cluster, so remove it from current cluster.
            # this will be a valid cluster after deleting a line.
            # add current cluster - it's first line.
            vertical_clusters.append(
                Cluster(members=cluster.members[1:], page_bbox=page.bbox)
            )

    # initialize first cluster with first line on page.
    cluster_lines = [page.lines[0]]
    for line in page.lines[1:]:
        # check if size of whitespace below this line is within 5% of the same as the cluster's average whitespace below..
        if (
            abs(
                fraction_different(
                    mean([l.whitespace_below for l in cluster_lines]),
                    line.whitespace_below,
                )
            )
            >= 0.05
        ):
            # whitespace below this line is different than cluster's standard whitespace below, so current line should be the last added to cluster group.
            # check if adding this line would make a valid cluster.
            if (
                # adding line would create a cluster > 2 lines, so cluster is valid regardless of weather line are separated by standard/expected whitespace.
                len(cluster_lines) > 1
                # only add two line cluster if the lines are separated by standard / expected space for that font size.
                or len(cluster_lines) == 1
                and line_spacing.is_expected_line_space(cluster_lines[-1], line)
            ):
                cluster_lines.append(line)
                _check_and_add(Cluster(cluster_lines, page.bbox))
            # else: this is a 2 line group with line separated by non-standard/expected whitespace, so this is not a valid cluster.
            # Use the last line to initialize the next cluster. This should be done because lines on boundaries can be valid members of two clusters. _check_and_add will take care of this issue.
            cluster_lines = [line]
        else:
            cluster_lines.append(line)
    # add last cluster.
    if len(cluster_lines) > 1:
        _check_and_add(Cluster(cluster_lines, page.bbox))
    return vertical_clusters
