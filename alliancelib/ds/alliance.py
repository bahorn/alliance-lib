# pylint: disable=C0103
"""
Builds upon VertexSets to implement the constraints we need to check various
alliance properties.
"""
import math
from typing import List, Dict
from itertools import combinations

from .types import NodeId, Graph
from .vertex_set import \
        ConstrainedVertexSet, VertexConstraint, ConstraintException


def neighbours_in_set(graph: Graph,
                      node: NodeId,
                      nodeset: List[NodeId]
                      ) -> int:
    """
    Find the number of neighbours `node` has in `nodeset`.
    """
    res = 0
    for potential_neighbour in nodeset:
        if graph.has_edge(node, potential_neighbour):
            res += 1
    return res


def threshold_constraint(thresholds: Dict) -> VertexConstraint:
    """
    Check if a vertex has enough neighbours in the set.
    """
    def threshold_constraint_function(graph: Graph,
                                      node: NodeId,
                                      nodeset: List[NodeId]
                                      ) -> bool:
        return neighbours_in_set(graph, node, nodeset) >= thresholds[node]

    return threshold_constraint_function


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


# Now we we define representations of Alliances that can only exist if they
# have been validated.


class ThresholdAlliance(ConstrainedVertexSet):
    """
    Validated representation of a threshold alliance.
    """

    def __init__(self, graph: Graph, indices: List[NodeId], thresholds: Dict):
        super().__init__(graph, indices, threshold_constraint(thresholds))


class DefensiveAlliance(ThresholdAlliance):
    """
    Validated representation of a defensive alliance.
    """

    def __init__(self, graph: Graph, indices: List[NodeId], r: int = -1):
        thresholds = {
            node: defensive_alliance_threshold(graph, node, r)
            for node in graph.nodes()
        }
        super().__init__(graph, indices, thresholds)


# These two need extra functions to verify the alliance

class NotLocallyMinimal(Exception):
    """
    Exception if an alliance is not Locally Minimal.
    """


class LocallyMinimalDefensiveAlliance(DefensiveAlliance):
    """
    Validated representation of a Locally Minimal Defensive Alliance.

    This is a Defensive Alliance where removing any single vertex won't also
    result in another Defensive Alliance.
    """

    def __init__(self, graph: Graph, indices: List[NodeId], r: int = -1):
        # attempt to create a Defensive Alliance based on the combinations of
        # vertices.
        # if one exists, we need to raise an exception
        for indices_set in combinations(indices, len(indices) - 1):
            try:
                DefensiveAlliance(graph, list(indices_set), r)
                raise NotLocallyMinimal()
            except ConstraintException:
                continue
        super().__init__(graph, indices, r)


class NotGloballyMinimal(Exception):
    """
    Exception if an alliance is not Globally Minimal.
    """


class GloballyMinimalDefensiveAlliance(DefensiveAlliance):
    """
    Validated representation of a Globally Minimal Defensive Alliance.

    This is a Defensive Alliance where no proper subset is also a Defensive
    Alliance.
    """

    def __init__(self, graph: Graph, indices: List[NodeId], r: int = -1):
        super().__init__(graph, indices, r)


# Conversion functions

def convert_ta_to_da(ta: ThresholdAlliance, r=-1) -> DefensiveAlliance:
    """
    Convert a ThresholdAlliance to a DefensiveAlliance
    """
    return DefensiveAlliance(ta.graph(), ta.vertices(), r)


__all__ = [
    'DefensiveAlliance',
    'ThresholdAlliance',
    'GloballyMinimalDefensiveAlliance',
    'LocallyMinimalDefensiveAlliance',
    'convert_ta_to_da',
    'defensive_alliance_threshold',
    'NotGloballyMinimal',
    'NotLocallyMinimal'
]
