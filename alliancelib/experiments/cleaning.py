"""
Graph Cleaning functions
"""
import random


def min_degree_add(g, degree):
    needs_neighbours = []
    for node in g.nodes:
        if g.degree(node) < degree:
            needs_neighbours.append(node)

    for node in needs_neighbours:
        potential_neighbours = set(g.nodes()) \
                - set(g.neighbors(node)) - set([node])
        needed = (degree - g.degree(node))
        if needed <= 0:
            continue
        for choice in random.sample(list(potential_neighbours), needed):
            g.add_edge(node, choice)

    return g


def remove_min_degree(g, degree):
    removed = 0

    while len(g.nodes) >= 0:
        to_remove = []

        for node in g.nodes:
            if g.degree(node) < degree:
                to_remove.append(node)

        if len(to_remove) == 0:
            break

        removed += len(to_remove)

        g.remove_nodes_from(to_remove)

    return g
