# pylint: disable=C0103
"""
This is a algorithm that removes vertices to try and find proper subsets that
can't be further reduced.

This is exponetial time, so it can't be ran on anything too large but is useful
to verify gadgets.
"""
from itertools import combinations

from typing import Optional
from alliancelib.ds import \
    Graph, \
    NodeId, \
    NodeSet, \
    VertexSet, \
    GloballyMinimalDefensiveAlliance, \
    convert_to_gmda, \
    chisel, \
    ProtectionFunction, \
    da_is_protected


def find_minimal_rec(graph: Graph,
                     protected: ProtectionFunction,
                     nodes: NodeSet
                     ) -> Optional[VertexSet]:
    """
    Recursive, but this algorithm is completely unsuited to cases where you
    would hit 1000 layers deep.

    The heat death of the universe will occur sooner than this returning in
    those cases.
    """
    hit = False

    for attempt in combinations(nodes, len(nodes) - 1):
        res = chisel(graph, protected, set(attempt))
        if res != set():
            hit = True
            vs = find_minimal_rec(graph, protected, res)
            if vs:
                return vs

    if not hit:
        return VertexSet(graph, nodes)

    return None


def find_minimal(graph: Graph,
                 protected: ProtectionFunction
                 ) -> Optional[VertexSet]:
    """
    Find a minimal alliance in a graph.
    """
    return find_minimal_rec(graph, protected, set(graph.nodes()))


def find_gmda(graph: Graph,
              r: int = -1
              ) -> Optional[GloballyMinimalDefensiveAlliance]:
    """
    Find a Globally Minimal Defensive Alliance
    """
    def protection_function(g: Graph, n: NodeId, ns: NodeSet):
        return da_is_protected(g, n, ns, r)

    res = find_minimal(graph, protection_function)
    if res:
        return convert_to_gmda(res)
    return None
