"""
Common functions that get used a lot.
"""
from collections.abc import Callable

from alliancelib.ds.types import NodeId, Graph, NodeSet

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


__all__ = [
    'neighbours_in_set',
    'neighbours_in_set_count',
    'ProtectionFunction'
]
