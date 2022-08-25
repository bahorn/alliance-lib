# pylint: disable=C0103
"""
Globally Minimal Defensive Alliance Representation
"""
from itertools import combinations

from alliancelib.ds.types import NodeId, Graph, NodeSet

from .da import DefensiveAlliance, da_is_protected
from .common import ProtectionFunction


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


__all__ = [
    'GloballyMinimalDefensiveAlliance',
    'NotGloballyMinimal',
    'chisel'
]
