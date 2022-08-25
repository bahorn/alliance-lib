# pylint: disable=C0103
"""
Defensive Alliance representation
"""
import math

from alliancelib.ds.types import NodeId, Graph, NodeSet
from alliancelib.ds.vertex_set import ConstraintException

from .threshold import ThresholdAlliance
from .common import neighbours_in_set_count


def defensive_alliance_threshold(graph: Graph,
                                 node: NodeId,
                                 r: int = -1
                                 ) -> int:
    """
    Compute the threshold for a r-Defensive Alliance
    """
    neighbour_count = len(list(graph.neighbors(node)))
    # The iterative, somewhat more initutive approach is:
    # for i in range(0, neighbour_count + 1):
    #    if i >= ((neighbour_count - i) + r):
    #        return i
    # but that is slow, so it is reduced to:
    return math.ceil((neighbour_count + r) / 2)


def da_is_protected(graph: Graph, node: NodeId, nodes: NodeSet, r: int = -1):
    """
    Check if a vertex is protected.
    """
    return neighbours_in_set_count(graph, node, nodes) >= \
        defensive_alliance_threshold(graph, node, r)


# Now we we define representations of Alliances that can only exist if they
# have been validated.


class DefensiveAlliance(ThresholdAlliance):
    """
    Validated representation of a defensive alliance.
    """

    def __init__(self, graph: Graph, indices: NodeSet, r: int = -1):
        if len(indices) == 0:
            raise ConstraintException

        thresholds = {
            node: defensive_alliance_threshold(graph, node, r)
            for node in graph.nodes()
        }
        super().__init__(graph, indices, thresholds)


# Test functions

def is_defensive_alliance(graph: Graph, nodes: NodeSet, r: int) -> bool:
    """
    Check if a set of vertices is an alliance.
    """
    try:
        DefensiveAlliance(graph, nodes, r)
        return True
    except ConstraintException:
        return False


__all__ = [
    'DefensiveAlliance',
    'defensive_alliance_threshold',
    'is_defensive_alliance',
    'da_is_protected'
]
