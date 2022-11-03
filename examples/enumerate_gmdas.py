#!/usr/bin/env python3
"""
Machine checking some graphs to confirm they have they properties we want for a
reduction.
"""
import copy
import itertools
import sys
import networkx as nx

from alliancelib.ds import VertexSet
from alliancelib.ds.alliances.conversion import convert_to_gmda
from alliancelib.vis.vertexset import display


def is_protected(graph, vertex, subset):
    """
    check if a vertex is protected
    """
    inside = 0
    outside = 0
    for neighbour in graph.neighbors(vertex):
        if neighbour in subset:
            inside += 1
            continue
        outside += 1
    return inside >= (outside - 1)


def remove_unprotected(graph, subset):
    """
    Finds unprotected vertices, and removes them.
    """
    subset_ = copy.copy(subset)
    while True:
        to_remove = []
        for vertex in subset_:
            if not is_protected(graph, vertex, subset_):
                to_remove.append(vertex)
        if len(to_remove) == 0:
            break
        subset_ = [vertex for vertex in subset_ if vertex not in to_remove]
    return subset_


def minimal(graph, subset):
    """
    Checks if a subset is minimal.
    """
    # try removing each vertex, if they all return nothing we have a minimal
    # alliance.
    minimal_alliances = set()
    nonminimal_alliances = set()
    skip = False
    for subset_ in itertools.combinations(subset, len(subset) - 1):
        subset_ = remove_unprotected(graph, subset_)
        if len(subset_) > 0:
            skip = True
            nonminimal_alliances.add(tuple(subset_))

    if not skip:
        minimal_alliances.add(tuple(subset))

    return (minimal_alliances, nonminimal_alliances)


def find_minimal(graph):
    """
    Find the minimal alliances in a graph.
    """
    # get the initial set of nodes
    # - remove all vertices with a degree of 1, as they are minimal alliances
    # on their own.
    # - remove any unprotected vertices that this causes.
    nodes = remove_unprotected(
        graph,
        [node for node in graph.nodes if graph.degree(node) > 1]
    )
    minimal_alliances, nonminimal_alliances = minimal(graph, nodes)

    while len(nonminimal_alliances) > 0:
        new_nonminimal = set()
        for alliance in nonminimal_alliances:
            ma, nma = minimal(graph, alliance)
            for a in ma:
                minimal_alliances.add(tuple(a))
            for a in nma:
                new_nonminimal.add(tuple(a))
        nonminimal_alliances = new_nonminimal

    for node in graph.nodes:
        if graph.degree(node) <= 1:
            minimal_alliances.add(tuple([node]))
    return minimal_alliances


def main(filename):
    """
    main
    """
    graph = nx.read_graphml(filename)
    graph = nx.convert_node_labels_to_integers(graph)
    minimal_subsets = find_minimal(graph)
    for subset in minimal_subsets:
        if len(subset) > 2:
            gmda = convert_to_gmda(VertexSet(graph, subset))
            display(gmda)


if __name__ == "__main__":
    main(sys.argv[1])
