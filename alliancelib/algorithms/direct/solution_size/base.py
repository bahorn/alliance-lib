# pylint: disable=C0103,R0913
"""
Searches for alliances up to a certain solution size.

This is in FPT for many cases, include Defensive Alliance.
This is because you can ignore vertices that would add too many neighbours,
caping the total number of vertices to consider.
"""
from typing import Optional
from alliancelib.ds import \
    Graph, \
    NodeSet, \
    VertexSet

from .common import VertexPredicate, SolutionPredicate


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


def alliance_solution_size(graph: Graph,
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


__all__ = [
    'alliance_solution_size'
]
