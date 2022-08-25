# pylint: disable=C0103
"""
Builds upon VertexSets to implement the constraints we need to check various
alliance properties.
"""
import math
from collections.abc import Callable
from typing import Dict
from itertools import combinations

from .types import NodeId, Graph, NodeSet
from .vertex_set import \
    VertexSet, \
    ConstrainedVertexSet, \
    VertexConstraint, \
    ConstraintException

ProtectionFunction = Callable[[Graph, NodeId, NodeSet], bool]


def neighbours_in_set(graph: Graph, node: NodeId, nodeset: NodeSet) -> NodeSet:
    """
    Find a set of neighbours in the nodeset for `node`.
    """
    res: NodeSet = set()
    for potential_neighbour in filter(lambda x: x != node, nodeset):
        if graph.has_edge(node, potential_neighbour):
            res = res.union({potential_neighbour})
    return res


def neighbours_in_set_count(graph: Graph,
                            node: NodeId,
                            nodeset: NodeSet
                            ) -> int:
    """
    Find the number of neighbours `node` has in `nodeset`.
    """
    return sum(
        graph.has_edge(node, potential_neighbour)
        for potential_neighbour in filter(lambda x: x != node, nodeset)
    )


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


class ThresholdAlliance(ConstrainedVertexSet):
    """
    Validated representation of a threshold alliance.
    """

    def __init__(self, graph: Graph, indices: NodeSet, thresholds: Dict):
        super().__init__(graph, indices, threshold_constraint(thresholds))


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

    def __init__(self, graph: Graph, indices: NodeSet, r: int = -1):
        # attempt to create a Defensive Alliance based on the combinations of
        # vertices.
        # if one exists, we need to raise an exception
        for indices_set in combinations(indices, len(indices) - 1):
            try:
                DefensiveAlliance(graph, set(indices_set), r)
                raise NotLocallyMinimal()
            except ConstraintException:
                continue
        super().__init__(graph, indices, r)


class NotGloballyMinimal(Exception):
    """
    Exception if an alliance is not Globally Minimal.
    """


def chisel(graph: Graph,
           protected: ProtectionFunction,
           nodes: NodeSet
           ) -> NodeSet:
    """
    Remove unprotected vertices.
    """
    prev: NodeSet = set()
    curr: NodeSet = nodes

    # find and remove all the unprotected vertices.
    while prev != curr:
        prev = curr
        curr = set(filter(
            lambda v: protected(graph, v, curr),
            curr
        ))

    return curr


class GloballyMinimalDefensiveAlliance(DefensiveAlliance):
    """
    Validated representation of a Globally Minimal Defensive Alliance.

    This is a Defensive Alliance where no proper subset is also a Defensive
    Alliance.
    """

    def __init__(self, graph: Graph, indices: NodeSet, r: int = -1):
        super().__init__(graph, indices, r)

        def protection_function(g: Graph, n: NodeId, ns: NodeSet):
            return da_is_protected(g, n, ns, r)

        for test in combinations(indices, len(indices) - 1):
            if chisel(graph, protection_function, set(test)) != set():
                raise NotGloballyMinimal()


# Conversion functions

def convert_to_da(vs: VertexSet, r: int = -1) -> DefensiveAlliance:
    """
    Convert a VertexSet to a DefensiveAlliance
    """
    return DefensiveAlliance(vs.graph(), vs.vertices(), r)


def convert_to_gmda(vs: VertexSet,
                    r: int = -1
                    ) -> GloballyMinimalDefensiveAlliance:
    """
    Convert a VertexSet to a DefensiveAlliance
    """
    return GloballyMinimalDefensiveAlliance(vs.graph(), vs.vertices(), r)


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
    'ThresholdAlliance',
    'GloballyMinimalDefensiveAlliance',
    'LocallyMinimalDefensiveAlliance',
    'convert_to_da',
    'convert_to_gmda',
    'defensive_alliance_threshold',
    'NotGloballyMinimal',
    'NotLocallyMinimal',
    'is_defensive_alliance',
    'neighbours_in_set',
    'neighbours_in_set_count',
    'da_is_protected',
    'chisel',
    'ProtectionFunction'
]
