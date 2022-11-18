# pylint: disable=C0103,R0913
"""
Searches for Defensive Alliances up to a certain solution size.
"""
from typing import Optional
from alliancelib.ds.types import Graph, NodeId, NodeSet
from alliancelib.ds.alliances.da import \
    DefensiveAlliance, \
    is_defensive_alliance, \
    defensive_alliance_threshold
from alliancelib.ds.alliances.conversion import convert_to_da


from .base import \
        alliance_solution_size, \
        alliance_solution_size_parallel, \
        traverse


def defensive_alliance(graph: Graph,
                       k: int,
                       r: int = -1,
                       initial = None
                       ) -> Optional[DefensiveAlliance]:
    """
    Find a DefensiveAlliance up to `k` vertices in size.

    FPT running time.
    """

    def vertex_predicate(g: Graph, v: NodeId, d: int):
        return defensive_alliance_threshold(g, v, r) <= d

    def solution_predicate(g: Graph, v: NodeSet):
        return is_defensive_alliance(g, v, r)

    res = None

    if initial:
        res = traverse(
            graph, set(), set(initial), vertex_predicate, solution_predicate, k
        )
    else:
        res = alliance_solution_size(
            graph, vertex_predicate, solution_predicate, k
        )

    if res:
        return convert_to_da(res, r)

    return None


def defensive_alliance_parallel(graph: Graph,
                                k: int,
                                r: int = -1,
                                initial = [],
                                threads: int = 1
                                ) -> Optional[DefensiveAlliance]:
    """
    Find a DefensiveAlliance up to `k` vertices in size.

    FPT running time.
    """

    def vertex_predicate(g: Graph, v: NodeId, d: int):
        return defensive_alliance_threshold(g, v, r) <= d

    def solution_predicate(g: Graph, v: NodeSet):
        return is_defensive_alliance(g, v, r)

    res = alliance_solution_size_parallel(
        graph, initial, vertex_predicate, solution_predicate, k, threads
    )

    if res:
        return convert_to_da(res, r)

    return None


__all__ = [
    'defensive_alliance',
    'defensive_alliance_parallel'
]
