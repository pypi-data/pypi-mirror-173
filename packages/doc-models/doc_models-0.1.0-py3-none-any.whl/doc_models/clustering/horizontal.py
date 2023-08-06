from typing import Dict, List

from doc_models.components.cluster import Cluster


def horizontal_alignment(
    cluster1: "Cluster", cluster2: "Cluster", max_diff=3
) -> Dict[str, float]:
    "Return dict containing alignment measurements for any axes where clusters are aligned."
    alignment = {}
    # check if cluster is left aligned.
    left_alignment = abs(cluster1.left - cluster2.left)
    if left_alignment < max_diff:
        alignment["left_alignment"] = left_alignment
    # check if cluster is right aligned.
    right_alignment = abs(cluster1.right - cluster2.right)
    if right_alignment < max_diff:
        alignment["right_alignment"] = right_alignment
    # check if cluster is x_center aligned.
    x_center_alignment = abs(cluster1.x_center - cluster2.x_center)
    if x_center_alignment < max_diff:
        alignment["x_center_alignment"] = x_center_alignment
    if "left_alignment" not in alignment and "right_alignment" not in alignment:
        # check for symmetry.
        left_pos_diff = cluster1.left - cluster2.left
        right_pos_diff = cluster1.right - cluster2.right
        # should have about same magnitude, but opposite sign.
        left_pos_diff + right_pos_diff < max_diff
        alignment["center_symmetry"] = (abs(left_pos_diff) + abs(right_pos_diff)) / 2
    return alignment


def add_to_column(cluster, column: List[Dict[str, float]]) -> bool:
    """Add cluster to column if cluster is aligned with column on at least one axis.
    Return True if cluster is added to column.
    """
    # if aligned with last column cluster, store alignment measurements.
    cluster_align = get_cluster_alignment(cluster, column[-1]["cluster"])
    if len(cluster_align):
        # cluster has alignment, so add it to the column.
        cluster_align["cluster"] = cluster
        column.append(cluster_align)
        return True
    return False


def start_new_column(cluster1, cluster2) -> Union[List[Dict[str, float]], None]:
    """Initialize a new column with cluster1 and cluster2 if clusters are aligned on at least one axis.
    Return True if a new column was initialized.
    """
    cluster_alignment = get_cluster_alignment(cluster1, cluster2)
    if len(cluster_alignment):
        # clusters have alignment, so start a new active column with these two clusters.
        cluster_alignment["cluster"] = cluster2
        # column members store alignment measures with column cluster above, so first member has no alignment measures.
        return [{"cluster": cluster1}, cluster_alignment]


def get_finished_clusters(
    active_cluster_groups: List[List[Cluster]], cur_line_idx: int
) -> List[Cluster]:
    """Split cluster list into a list of finished cluster and unfinished clusters.
    Clusters are finished when we reach a line index greater than highest line index in cluster + 1
    """
    clusters, unfinished = [], []
    for cluster_group in active_cluster_groups:
        end_line_idx = max(c.end_line_idx for c in cluster_group)
        if cur_line_idx - end_line_idx > 1:
            clusters.append(Cluster.from_clusters(cluster_group))
        else:
            unfinished.append(cluster_group)
    return clusters, unfinished


def cluster_uniform_horizontal_spacing(clusters, check_children: bool):
    parent_clusters: List[Cluster] = []
    active_parent_clusters: List[List[Cluster]] = []
    # sort clusters by start line index (lowest to highest)
    clusters.sort(key=lambda c: c.start_line_idx)
    for next_idx, cluster in enumerate(clusters[:-1], start=1):
        new_clusters, active_parent_clusters = get_finished_clusters(
            active_parent_clusters, cluster.start_line_idx
        )
        parent_clusters += new_clusters
        to_check = cluster.children if check_children else [cluster]
        for c in to_check:
            pass


def cluster_uniform_horizontal_spacing(clusters, check_children: bool):
    finished_clusters, unfinished_clusters = [], []
    for next_idx, cluster in enumerate(clusters[:-1], start=1):
        if required_type is None or cluster.type in required_type:
            new_finished, unfinished_clusters = find_finished_clusters(
                unfinished_clusters, cluster.end_line_idx
            )
            finished_clusters += new_finished
            to_check = cluster.children if check_children else [cluster]
            for c in to_check:
                # check if cluster aligns with any current column.
                if not any(
                    add_to_column(c, col) for col in unfinished_columns
                ) and next_idx < len(clusters):
                    next_cluster = clusters[next_idx]
                    next_to_check = (
                        next_cluster.children if check_children else [next_cluster]
                    )
                    for nc in next_to_check:
                        start_new_column(c, nc)
    # reached end, so all clusters must be finished.
    horizontal_clusters += unfinished_columns
    return horizontal_clusters
