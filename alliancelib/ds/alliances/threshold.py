"""
Threshold Alliance Representation
"""
from typing import Dict

from alliancelib.ds.types import NodeId, Graph, NodeSet
from alliancelib.ds.vertex_set import \
    ConstrainedVertexSet, \
    VertexConstraint

from .common import neighbours_in_set_count


def threshold_constraint(thresholds: Dict) -> VertexConstraint:
    """
    Check if a vertex has enough neighbours in the set.
    """
    def threshold_constraint_function(graph: Graph,
                                      node: NodeId,
                                      nodeset: NodeSet
                                      ) -> bool:
        return neighbours_in_set_count(graph, node, nodeset) \
                >= thresholds[node]

    return threshold_constraint_function


# Now we we define representations of Alliances that can only exist if they
# have been validated.
class ThresholdAlliance(ConstrainedVertexSet):
    """
    Validated representation of a threshold alliance.
    """

    def __init__(self, graph: Graph, indices: NodeSet, thresholds: Dict):
        super().__init__(graph, indices, threshold_constraint(thresholds))


__all__ = [
    'ThresholdAlliance',
    'threshold_constraint'
]
