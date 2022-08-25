# pylint: disable=C0103,R0913
"""
Searches for alliances up to a certain solution size.

This is in FPT for many cases, include Defensive Alliance.
This is because you can ignore vertices that would add too many neighbours,
caping the total number of vertices to consider.
"""
from typing import Any, Optional
from collections.abc import Callable
from alliancelib.ds import \
    Graph, \
    NodeId, \
    NodeSet, \
    VertexSet, \
    DefensiveAlliance, \
    is_defensive_alliance, \
    defensive_alliance_threshold, \
    convert_to_da

VertexPredicate = Callable[[Graph, NodeId, Any], bool]
SolutionPredicate = Callable[[Graph, NodeSet], bool]


def traverse(graph: Graph,
             initial_set: NodeSet,
             possible_vertices: NodeSet,
             vertex_predicate: VertexPredicate,
             solution_predicate: SolutionPredicate,
             depth: int
             ) -> Optional[VertexSet]:
    """
    Recursive function, as thats the cleanest way of writing this, and you'll
    never actually hit the python stack limit of ~1000.
    """
    if solution_predicate(graph, initial_set):
        return VertexSet(graph, initial_set)

    if depth <= 0:
        return None

    # compute the potential set of neighbours.
    neighbours: NodeSet = set()
    for vertex in initial_set:
        neighbours = neighbours.union(set(graph.neighbors(vertex)))
    neighbours -= initial_set

    if len(initial_set) == 0:
        neighbours = possible_vertices
    else:
        pass

    neighbours_ = filter(
        lambda v: vertex_predicate(graph, v, depth),
        neighbours
    )

    for vertex in neighbours_:
        vs = {vertex}
        res = traverse(
            graph,
            initial_set.union(vs),
            possible_vertices - vs,
            vertex_predicate,
            solution_predicate,
            depth - 1
        )
        if res:
            return res

    return None


def alliance_solution_size(
                           graph: Graph,
                           vertex_predicate: VertexPredicate,
                           solution_predicate: SolutionPredicate,
                           k: int
                           ) -> Optional[VertexSet]:
    """
    Finds a connected alliance, up to a certain size.
    """
    # first, find the vertices that satify the predicate.
    possible_vertices = set(
        filter(lambda v: vertex_predicate(graph, v, k), graph.nodes())
    )

    return traverse(
        graph,
        set(),
        possible_vertices,
        vertex_predicate,
        solution_predicate,
        k
    )


def defensive_alliance_solution_size(
                                     graph: Graph,
                                     k: int,
                                     r: int = -1
                                     ) -> Optional[DefensiveAlliance]:
    """
    Find a DefensiveAlliance up to `k` vertices in size.

    FPT running time.
    """

    def vertex_predicate(g: Graph, v: NodeId, d: int):
        return defensive_alliance_threshold(g, v, r) < d

    def solution_predicate(g: Graph, v: NodeSet):
        return is_defensive_alliance(g, v, r)

    res = alliance_solution_size(
        graph, vertex_predicate, solution_predicate, k
    )

    if res:
        return convert_to_da(res, r)

    return None


__all__ = [
    'defensive_alliance_solution_size',
    'alliance_solution_size',
    'VertexPredicate',
    'SolutionPredicate'
]
